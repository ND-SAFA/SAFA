package edu.nd.crc.safa.server.repositories;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.AppConstraints;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.delta.EntityDelta;
import edu.nd.crc.safa.server.entities.app.delta.ModifiedEntity;
import edu.nd.crc.safa.server.entities.app.project.IAppEntity;
import edu.nd.crc.safa.server.entities.db.CommitError;
import edu.nd.crc.safa.server.entities.db.IBaseEntity;
import edu.nd.crc.safa.server.entities.db.IVersionEntity;
import edu.nd.crc.safa.server.entities.db.ModificationType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.VersionEntityAction;
import edu.nd.crc.safa.server.repositories.artifacts.IVersionRepository;
import edu.nd.crc.safa.utilities.ProjectVersionFilter;

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

    /**
     * @param project The project whose entities are retrieved.
     * @return Returns all versions of the base entities in a project.
     */
    protected abstract List<V> retrieveVersionEntitiesByProject(Project project);

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
    protected abstract Optional<B> findBaseEntityById(String baseEntityId);

    /**
     * Creates or updates any entities related to AppEntity and returns the corresponding base entity.
     *
     * @param projectVersion    The project version associated with given app entity.
     * @param artifactAppEntity The application entity whose sub entities are being created.
     * @return Returns the base entity associated with given app entity.
     */
    protected abstract B createOrUpdateRelatedEntities(ProjectVersion projectVersion,
                                                       A artifactAppEntity) throws SafaError;

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

    protected abstract V save(V versionEntity);

    @Override
    public List<A> retrieveAppEntitiesByProjectVersion(ProjectVersion projectVersion) {
        List<V> artifactBodies = this.retrieveVersionEntitiesByProjectVersion(projectVersion);
        List<A> artifacts = new ArrayList<>();
        for (V artifactVersion : artifactBodies) {
            artifacts.add(this.retrieveAppEntityFromVersionEntity(artifactVersion));
        }
        return artifacts;
    }

    /**
     * Calculates contents of each artifact at given version and returns bodies at version.
     *
     * @param projectVersion - The version of the artifact bodies that are returned
     * @return list of artifact bodies in project at given version
     */
    @Override
    public List<V> retrieveVersionEntitiesByProjectVersion(ProjectVersion projectVersion) {
        Map<String, List<V>> entityHashTable =
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
        String entityId) {
        List<V> versionEntities = this.retrieveVersionEntitiesByProject(projectVersion.getProject())
            .stream()
            .filter(versionEntity -> versionEntity.getBaseEntityId().equals(entityId))
            .collect(Collectors.toList());
        Map<String, List<V>> entityHashTable = new HashMap<>();
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
                                                                A appEntity) {
        VersionEntityAction<V> versionEntityAction = () -> {
            B b = this.createOrUpdateRelatedEntities(
                projectVersion,
                appEntity);

            V versionEntity = this.instantiateVersionEntityFromAppEntity(
                projectVersion,
                b,
                appEntity);

            if (versionEntity.getModificationType() != ModificationType.NO_MODIFICATION) {
                createOrUpdateVersionEntity(versionEntity);
                String baseEntityId = b.getBaseEntityId();
                appEntity.setBaseEntityId(baseEntityId);
            }

            return Optional.of(versionEntity);
        };
        String baseEntityId = appEntity.getBaseEntityId();
        return commitErrorHandler(projectVersion, versionEntityAction, baseEntityId, this.getProjectActivity());
    }

    @Override
    public Pair<V, CommitError> deleteVersionEntityByBaseEntityId(
        ProjectVersion projectVersion,
        String baseEntityId) {
        VersionEntityAction<V> versionEntityAction = () -> {
            Optional<B> baseEntityOptional = this.findBaseEntityById(baseEntityId);

            if (baseEntityOptional.isPresent()) {
                B b = baseEntityOptional.get();
                V removedVersionEntity = this.instantiateVersionEntityFromAppEntity(
                    projectVersion,
                    b,
                    null);
                this.createOrUpdateVersionEntity(removedVersionEntity);
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
        Map<String, A> addedEntities = new HashMap<>();
        Map<String, ModifiedEntity<A>> modifiedEntities = new HashMap<>();
        Map<String, A> removedEntities = new HashMap<>();

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
            String baseEntityId = b.getBaseEntityId();

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
                    throw new SafaError("Missing case in switch for modification type:" + modificationType);
            }
        }

        return new EntityDelta<>(addedEntities, modifiedEntities, removedEntities);
    }

    /**
     * Commits list of given application entities
     *
     * @param projectVersion The version whose app entities are retrieved.
     * @param appEntities    The set of all artifacts existing in given project version.
     * @return List of pairs of VersionEntities or commit errors
     */

    @Override
    public List<Pair<V, CommitError>> commitAllAppEntitiesToProjectVersion(
        ProjectVersion projectVersion,
        List<A> appEntities) {

        List<String> processedAppEntities = new ArrayList<>();
        List<Pair<V, CommitError>> response = appEntities
            .stream()
            .map(a -> this.commitAppEntityToProjectVersion(projectVersion, a))
            .peek(commitResponse -> {
                if (commitResponse.getValue1() == null) {
                    processedAppEntities.add(commitResponse.getValue0().getBaseEntityId());
                }
            }).collect(Collectors.toList());

        List<Pair<V, CommitError>> removedVersionEntities = this.retrieveBaseEntitiesByProject(
                projectVersion.getProject())
            .stream()
            .filter(b -> !processedAppEntities.contains(b.getBaseEntityId()))
            .map(b -> this.deleteVersionEntityByBaseEntityId(
                projectVersion,
                b.getBaseEntityId()))
            .collect(Collectors.toList());
        response.addAll(removedVersionEntities);

        return response;
    }

    private void createOrUpdateVersionEntity(V versionEntity) throws SafaError {
        try {
            this.findExistingVersionEntity(versionEntity)
                .ifPresent(existingVersionEntity ->
                    versionEntity.setVersionEntityId(existingVersionEntity.getVersionEntityId()));
            this.save(versionEntity);
        } catch (Exception e) {
            String name = versionEntity.getBaseEntityId();
            String error = String.format("An error occurred while saving version entity with base id: %s", name);
            throw new SafaError(error, e);
        }
    }

    private Triplet<V, V, ModificationType> calculateDeltaEntityBetweenProjectVersions(
        B b,
        ProjectVersion baseVersion,
        ProjectVersion targetVersion) {
        List<V> bodies = this.retrieveVersionEntitiesByBaseEntity(b);

        V beforeEntity = this.getEntityAtVersion(bodies,
            baseVersion);
        V afterEntity = this.getEntityAtVersion(bodies,
            targetVersion);

        ModificationType modificationType = this
            .calculateModificationType(beforeEntity, afterEntity);
        return new Triplet<>(beforeEntity, afterEntity, modificationType);
    }

    private Pair<V, CommitError> commitErrorHandler(ProjectVersion projectVersion,
                                                    VersionEntityAction<V> versionEntityAction,
                                                    String entityName,
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
     * Returns the most recent entity version that passes given filter
     *
     * @param bodies The bodies to filter through
     * @param filter The filter deciding whether an entity's version is valid.
     * @return The latest entity version passing given filter.
     */
    private V getLatestEntityVersionWithFilter(List<V> bodies,
                                               ProjectVersionFilter filter) {
        V closestBodyToVersion = null;
        for (int i = bodies.size() - 1; i >= 0; i--) {
            V currentBody = bodies.get(i);
            ProjectVersion currentBodyVersion = currentBody.getProjectVersion();
            if (filter.shouldKeep(currentBodyVersion)) {
                if (closestBodyToVersion == null) {
                    closestBodyToVersion = currentBody;
                } else if (currentBodyVersion.isGreaterThan(closestBodyToVersion.getProjectVersion())
                ) {
                    closestBodyToVersion = currentBody;
                }
            }
        }
        return closestBodyToVersion;
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
        Map<String, List<V>> nameToVersionEntityMap) {
        List<V> entityVersionsAtProjectVersion = new ArrayList<>();

        for (Map.Entry<String, List<V>> entry : nameToVersionEntityMap.entrySet()) {
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

    private Map<String, List<V>> groupEntityVersionsByEntityId(ProjectVersion projectVersion) {
        Map<String, List<V>> entityHashtable = new HashMap<>();
        List<V> versionEntities = this.retrieveVersionEntitiesByProject(projectVersion.getProject());
        for (V versionEntity : versionEntities) {
            String entityId = versionEntity.getBaseEntityId();
            if (entityHashtable.containsKey(entityId)) {
                entityHashtable.get(entityId).add(versionEntity);
            } else {
                List<V> newList = new ArrayList<>();
                newList.add(versionEntity);
                entityHashtable.put(entityId, newList);
            }
        }
        return entityHashtable;
    }

    private V getEntityAtVersion(List<V> bodies, ProjectVersion version) {
        return this
            .getLatestEntityVersionWithFilter(bodies, target -> target.isLessThanOrEqualTo(version));
    }

    private V getEntityBeforeVersion(List<V> bodies, ProjectVersion version) {
        return this.getLatestEntityVersionWithFilter(bodies, target -> target.isLessThan(version));
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
        V previousBody =
            getEntityBeforeVersion(this.retrieveVersionEntitiesByBaseEntity(b), projectVersion);
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
}
