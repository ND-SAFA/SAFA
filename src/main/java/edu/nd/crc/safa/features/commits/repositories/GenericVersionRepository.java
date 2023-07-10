package edu.nd.crc.safa.features.commits.repositories;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.AppConstraints;
import edu.nd.crc.safa.features.artifacts.repositories.IVersionRepository;
import edu.nd.crc.safa.features.commits.entities.db.VersionEntityAction;
import edu.nd.crc.safa.features.common.IBaseEntity;
import edu.nd.crc.safa.features.common.IVersionEntity;
import edu.nd.crc.safa.features.delta.entities.app.EntityDelta;
import edu.nd.crc.safa.features.delta.entities.app.ModifiedEntity;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.errors.entities.db.CommitError;
import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.entities.db.ProjectEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.VersionCalculator;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import com.fasterxml.jackson.core.JsonProcessingException;
import org.javatuples.Pair;
import org.javatuples.Triplet;
import org.springframework.dao.DataIntegrityViolationException;

/**
 * Implements the generic logic for retrieving, creating, and modifying versioned entities.
 *
 * @param <V> The versioned entity.
 */
public abstract class GenericVersionRepository<
    B extends IBaseEntity,
    V extends IVersionEntity<A>,
    A extends IAppEntity>
    implements IVersionRepository<V, A> {

    VersionCalculator versionCalculator = new VersionCalculator();

    protected abstract V save(V versionEntity);

    @Override
    public List<A> retrieveAppEntitiesByProjectVersion(ProjectVersion projectVersion) {
        List<V> versionEntities = this.retrieveVersionEntitiesByProjectVersion(projectVersion);
        return versionEntities.stream()
            .map(this::retrieveAppEntityFromVersionEntity)
            .collect(Collectors.toList());
    }

    @Override
    public List<A> retrieveAppEntitiesByProject(Project project) {
        List<V> versions = retrieveVersionEntitiesByProject(project);
        return versions.stream()
            .map(this::retrieveAppEntityFromVersionEntity)
            .collect(Collectors.toList());
    }

    /**
     * Calculates contents of each artifact at given version and returns bodies at version.
     *
     * @param projectVersion - The version of the artifact bodies that are returned
     * @return list of artifact bodies in project at given version
     */
    @Override
    public List<V> retrieveVersionEntitiesByProjectVersion(ProjectVersion projectVersion) {
        Map<UUID, List<V>> entityHashTable =
            this.groupEntityVersionsByEntityId(projectVersion);
        return this.calculateVersionEntitiesAtProjectVersion(projectVersion, entityHashTable);
    }

    /**
     * Calculates contents of each artifact at given version and returns bodies at version.
     *
     * @param projectVersion - The version of the artifact bodies that are returned
     * @return list of artifact bodies in project at given version
     */
    @Override
    public Optional<V> findVersionEntityByProjectVersionAndBaseEntityId(
        ProjectVersion projectVersion,
        UUID entityId) {
        List<V> versionEntities = this.retrieveVersionEntitiesByProject(projectVersion.getProject())
            .stream()
            .filter(versionEntity -> versionEntity.getBaseEntityId().equals(entityId))
            .collect(Collectors.toList());
        Map<UUID, List<V>> entityHashTable = new HashMap<>();
        entityHashTable.put(entityId, versionEntities);
        List<V> currentVersionQuery = this.calculateVersionEntitiesAtProjectVersion(projectVersion,
            entityHashTable);
        return currentVersionQuery.isEmpty() ? Optional.empty() : Optional.of(currentVersionQuery.get(0));
    }

    /**
     * Commits the current state of app entity to given project version. AppEntity is modified
     * to contain the base entity id if created successfully. Warning, if submitted to an
     * non-current version changes are not propagated upstream.
     *
     * @param projectVersion The project version to save the changes to.
     * @param appEntity      The app entity whose state is saved.
     * @return String representing parser error if one occurred.
     */
    @Override
    public Pair<V, CommitError> commitAppEntityToProjectVersion(ProjectVersion projectVersion,
                                                                A appEntity, SafaUser user) {
        VersionEntityAction<V> versionEntityAction = () -> {
            B b = this.createOrUpdateRelatedEntities(projectVersion, appEntity, user);

            V versionEntity = this.instantiateVersionEntityFromAppEntity(
                projectVersion,
                b,
                appEntity);

            if (versionEntity.getModificationType() != ModificationType.NO_MODIFICATION) {
                createOrUpdateVersionEntity(versionEntity, user);
                UUID baseEntityId = b.getBaseEntityId();
                appEntity.setId(baseEntityId);
            }

            return Optional.of(versionEntity);
        };
        UUID baseEntityId = appEntity.getId();
        return commitErrorHandler(projectVersion, versionEntityAction, baseEntityId, this.getProjectActivity());
    }

    @Override
    public Pair<V, CommitError> deleteVersionEntityByBaseEntityId(
        ProjectVersion projectVersion,
        UUID baseEntityId,
        SafaUser user) {

        VersionEntityAction<V> versionEntityAction = () -> {
            Optional<B> baseEntityOptional = this.findBaseEntityById(baseEntityId);

            if (baseEntityOptional.isPresent()) {
                B b = baseEntityOptional.get();
                V removedVersionEntity = this.instantiateVersionEntityFromAppEntity(
                    projectVersion,
                    b,
                    null);
                this.createOrUpdateVersionEntity(removedVersionEntity, user);
                return removedVersionEntity == null ? Optional.empty() : Optional.of(removedVersionEntity);
            } else {
                return Optional.empty();
            }
        };
        return commitErrorHandler(projectVersion, versionEntityAction, baseEntityId, this.getProjectActivity());
    }

    @Override
    public EntityDelta<A> calculateEntityDelta(
        ProjectVersion baselineVersion,
        ProjectVersion targetVersion) {
        Project project = baselineVersion.getProject();
        Map<UUID, A> addedEntities = new HashMap<>();
        Map<UUID, ModifiedEntity<A>> modifiedEntities = new HashMap<>();
        Map<UUID, A> removedEntities = new HashMap<>();

        List<B> projectArtifacts = this.retrieveBaseEntitiesByProject(project);

        for (B b : projectArtifacts) {
            Triplet<V, V, ModificationType> delta = this
                .calculateDeltaEntityBetweenProjectVersions(
                    b,
                    baselineVersion,
                    targetVersion);
            ModificationType modificationType = delta.getValue2();
            if (modificationType == null) {
                continue;
            }
            UUID baseEntityId = b.getBaseEntityId();

            switch (modificationType) {
                case ADDED:
                    A appEntity = this.retrieveAppEntityFromVersionEntity(delta.getValue1());
                    addedEntities.put(baseEntityId, appEntity);
                    break;
                case MODIFIED:
                    A appBefore = this.retrieveAppEntityFromVersionEntity(delta.getValue0());
                    A appAfter = this.retrieveAppEntityFromVersionEntity(delta.getValue1());
                    ModifiedEntity<A> modifiedEntity = new ModifiedEntity<>(appBefore, appAfter);
                    modifiedEntities.put(baseEntityId, modifiedEntity);
                    break;
                case REMOVED:
                    A appRemoved = this.retrieveAppEntityFromVersionEntity(delta.getValue0());
                    removedEntities.put(baseEntityId, appRemoved);
                    break;
                default:
                    throw new SafaError("Missing case in switch for modification type: %s", modificationType);
            }
        }

        return new EntityDelta<>(addedEntities, modifiedEntities, removedEntities);
    }

    /**
     * Commits list of given application entities
     *
     * @param projectVersion The version whose app entities are retrieved.
     * @param appEntities    The set of all artifacts existing in given project version.
     * @param asCompleteSet  Whether appEntities are complete set of artifacts at project version
     * @return List of pairs of VersionEntities or commit errors
     */

    @Override
    public List<Pair<V, CommitError>> commitAllAppEntitiesToProjectVersion(
        ProjectVersion projectVersion,
        List<A> appEntities,
        boolean asCompleteSet,
        SafaUser user) {

        List<UUID> processedAppEntities = new ArrayList<>();
        List<Pair<V, CommitError>> response = appEntities
            .stream()
            .map(a -> {
                Pair<V, CommitError> commitResponse = this.commitAppEntityToProjectVersion(projectVersion, a, user);
                if (commitResponse.getValue1() == null) {
                    UUID baseEntityId = commitResponse.getValue0().getBaseEntityId();
                    processedAppEntities.add(baseEntityId);
                    a.setId(baseEntityId);
                }
                return commitResponse;
            })
            .collect(Collectors.toList());

        if (asCompleteSet) { // calculates deleted entities if this is complete set
            List<Pair<V, CommitError>> removedVersionEntities = this.retrieveBaseEntitiesByProject(
                    projectVersion.getProject())
                .stream()
                .filter(b -> !processedAppEntities.contains(b.getBaseEntityId()))
                .map(b -> this.deleteVersionEntityByBaseEntityId(
                    projectVersion,
                    b.getBaseEntityId(),
                    user))
                .collect(Collectors.toList());
            response.addAll(removedVersionEntities);
        }

        return response;
    }

    private void createOrUpdateVersionEntity(V versionEntity, SafaUser user) throws SafaError {
        try {
            Optional<V> previousEntity = this.findExistingVersionEntity(versionEntity);
            previousEntity.ifPresent(existingVersionEntity ->
                versionEntity.setVersionEntityId(existingVersionEntity.getVersionEntityId()));
            this.save(versionEntity);
            this.updateTimInfo(versionEntity.getProjectVersion(), versionEntity, previousEntity.orElse(null), user);
        } catch (Exception e) {
            e.printStackTrace();
            UUID baseEntityId = versionEntity.getBaseEntityId();
            String error = String.format("An error occurred while saving version entity with base id: %s",
                baseEntityId);
            throw new SafaError(error, e);
        }
    }

    private Triplet<V, V, ModificationType> calculateDeltaEntityBetweenProjectVersions(
        B b,
        ProjectVersion baseVersion,
        ProjectVersion targetVersion) {
        List<V> bodies = this.retrieveVersionEntitiesByBaseEntity(b);

        V beforeEntity = this.versionCalculator.getEntityAtVersion(bodies,
            baseVersion, IVersionEntity::getProjectVersion);
        V afterEntity = this.versionCalculator.getEntityAtVersion(bodies,
            targetVersion, IVersionEntity::getProjectVersion);

        ModificationType modificationType = this
            .calculateModificationType(beforeEntity, afterEntity);
        return new Triplet<>(beforeEntity, afterEntity, modificationType);
    }

    private Pair<V, CommitError> commitErrorHandler(ProjectVersion projectVersion,
                                                    VersionEntityAction<V> versionEntityAction,
                                                    UUID entityName,
                                                    ProjectEntity projectEntity) {
        String errorDescription = null;
        V versionEntity = null;
        CommitError commitError = null;
        try {
            Optional<V> versionEntityOptional = versionEntityAction.action();
            if (versionEntityOptional.isPresent()) {
                versionEntity = versionEntityOptional.get();
            } else {
                errorDescription = "Could not find a version entity of {" + entityName + "}";
            }
        } catch (DataIntegrityViolationException e) {
            e.printStackTrace();
            errorDescription =
                "Could not parse entity " + entityName + ": " + AppConstraints.getConstraintError(e);
        } catch (Exception e) {
            e.printStackTrace();
            errorDescription = e.getMessage();
        }
        if (errorDescription != null) {
            commitError = new CommitError(projectVersion, errorDescription, projectEntity);
        }
        return new Pair<>(versionEntity, commitError);
    }

    /**
     * Returns the type of modification made between the source and target entities.
     *
     * @param baseEntity   The original entity whose content is the base for calculating changes.
     * @param targetEntity The entity whose changes are compared against the base content.
     * @return The type of change occurring to base in order to reach target entity.
     */
    private ModificationType calculateModificationType(V baseEntity,
                                                       V targetEntity) {
        if (baseEntity == null || targetEntity == null) {
            if (baseEntity == targetEntity) {
                return null;
            } else if (baseEntity == null) {
                return ModificationType.ADDED;
            } else {
                return ModificationType.REMOVED;
            }
        } else {
            if (baseEntity.hasSameContent(targetEntity)) { // no change - same body
                return null;
            } else {
                if (targetEntity.getModificationType() == ModificationType.REMOVED) {
                    return ModificationType.REMOVED;
                } else if (baseEntity.getModificationType() == ModificationType.REMOVED) {
                    return ModificationType.ADDED;
                } else {
                    return ModificationType.MODIFIED;
                }
            }
        }
    }

    /**
     * Calculates the current version of artifact noted by the entries in the given map.
     *
     * @param projectVersion         The version returns for each entity in map.
     * @param nameToVersionEntityMap Contains artifact names as keys and their associated version entities as values.
     * @return List of version entities as showing up in given project version.
     */
    private List<V> calculateVersionEntitiesAtProjectVersion(
        ProjectVersion projectVersion,
        Map<UUID, List<V>> nameToVersionEntityMap) {
        List<V> entityVersionsAtProjectVersion = new ArrayList<>();

        for (Map.Entry<UUID, List<V>> entry : nameToVersionEntityMap.entrySet()) {
            V latest = null;
            for (V body : entry.getValue()) {
                if (body.getProjectVersion().isLessThanOrEqualTo(projectVersion)
                    && (latest == null || body.getProjectVersion().isGreaterThan(latest.getProjectVersion()))) {
                    latest = body;
                }
            }

            if (latest != null && latest.getModificationType() != ModificationType.REMOVED) {
                entityVersionsAtProjectVersion.add(latest);
            }
        }
        return entityVersionsAtProjectVersion;
    }

    private Map<UUID, List<V>> groupEntityVersionsByEntityId(ProjectVersion projectVersion) {
        List<V> versionEntities = this.retrieveVersionEntitiesByProject(projectVersion.getProject());
        return versionCalculator.groupEntityVersionsByEntityId(versionEntities, IVersionEntity::getBaseEntityId);
    }

    private V instantiateVersionEntityFromAppEntity(ProjectVersion projectVersion,
                                                    B b,
                                                    A appEntity) throws JsonProcessingException {
        ModificationType modificationType = this
            .calculateModificationTypeForAppEntity(projectVersion, b, appEntity);

        return this.instantiateVersionEntityWithModification(
            projectVersion,
            modificationType,
            b,
            appEntity);
    }

    private ModificationType calculateModificationTypeForAppEntity(ProjectVersion projectVersion,
                                                                   B b,
                                                                   A appEntity) {
        V previousBody = versionCalculator
            .getEntityBeforeVersion(this.retrieveVersionEntitiesByBaseEntity(b),
                projectVersion,
                IVersionEntity::getProjectVersion);
        if (previousBody == null) {
            return appEntity == null ? ModificationType.NO_MODIFICATION : ModificationType.ADDED;
        } else {
            if (appEntity == null) {
                boolean previouslyRemoved = previousBody.getModificationType() == ModificationType.REMOVED;
                return previouslyRemoved ? ModificationType.NO_MODIFICATION : ModificationType.REMOVED;
            } else { // app entity is not null
                if (previousBody.getModificationType() == ModificationType.REMOVED) {
                    return ModificationType.ADDED;
                }
                boolean hasSameContent = previousBody.hasSameContent(appEntity);
                return hasSameContent ? ModificationType.NO_MODIFICATION : ModificationType.MODIFIED;
            }
        }
    }

    /**
     * @param project The project whose entities are retrieved.
     * @return Returns all versions of the base entities in a project.
     */
    public abstract List<V> retrieveVersionEntitiesByProject(Project project);

    /**
     * @param entity The base entities whose versions are retrieved
     * @return List of versions associated with given base entities.
     */
    protected abstract List<V> retrieveVersionEntitiesByBaseEntity(B entity);

    /**
     * @param project The project whose entities are retrieved.
     * @return Returns list of base entities existing in project.
     */
    protected abstract List<B> retrieveBaseEntitiesByProject(Project project);

    /**
     * @param baseEntityId The name of the base entity.
     * @return Returns the base entity in given project with given name.
     */
    protected abstract Optional<B> findBaseEntityById(UUID baseEntityId);

    /**
     * Creates or updates any entities related to AppEntity and returns the corresponding base entity.
     *
     * @param projectVersion    The project version associated with given app entity.
     * @param artifactAppEntity The application entity whose sub entities are being created.
     * @param user The user doing the operation
     * @return Returns the base entity associated with given app entity.
     */
    protected abstract B createOrUpdateRelatedEntities(ProjectVersion projectVersion,
                                                       A artifactAppEntity, SafaUser user) throws SafaError;

    /**
     * Creates an entity version with content of app entity and containing
     * given modification type.
     *
     * @param projectVersion   The project version where version entity is created.
     * @param modificationType The type of change required to move from last commit to given app entity.
     * @param b                The base entity represented by app entity.
     * @param appEntity        The app entity whose content is being compared to previous commits.
     * @return The version entity for saving the app entity content to project version.
     */
    protected abstract V instantiateVersionEntityWithModification(ProjectVersion projectVersion,
                                                                  ModificationType modificationType,
                                                                  B b,
                                                                  A appEntity) throws JsonProcessingException;

    /**
     * Returns the type of project entity this version repository corresponds to.
     *
     * @return ProjectEntity associated with this repository.
     */
    protected abstract ProjectEntity getProjectActivity();

    /**
     * Given a VersionEntity this methods returns an optional possibly containing the source entity this
     * corresponds with.
     *
     * @param versionEntity The version entity being saved.
     * @return Optional possibly containing existing version entity.
     */
    protected abstract Optional<V> findExistingVersionEntity(V versionEntity);
}
