package edu.nd.crc.safa.features.commits.repositories;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
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
import edu.nd.crc.safa.features.projects.entities.db.ProjectEntityType;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.VersionCalculator;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.ProjectDataStructures;

import com.fasterxml.jackson.core.JsonProcessingException;
import org.javatuples.Pair;
import org.javatuples.Triplet;
import org.springframework.dao.DataIntegrityViolationException;

/**
 * Implements the generic logic for retrieving, creating, and modifying versioned entities.
 *
 * @param <VersionEntity> The versioned entity.
 */
public abstract class GenericVersionRepository<
    BaseEntity extends IBaseEntity,
    VersionEntity extends IVersionEntity<AppEntity>,
    AppEntity extends IAppEntity>
    implements IVersionRepository<VersionEntity, AppEntity> {

    private final VersionCalculator versionCalculator = new VersionCalculator();

    protected abstract VersionEntity save(VersionEntity versionEntity);

    @Override
    public List<AppEntity> retrieveAppEntitiesByProjectVersion(ProjectVersion projectVersion) {
        List<VersionEntity> versionEntities = this.retrieveVersionEntitiesByProjectVersion(projectVersion);
        return versionEntities.stream()
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
    public List<VersionEntity> retrieveVersionEntitiesByProjectVersion(ProjectVersion projectVersion) {
        Map<UUID, List<VersionEntity>> entityHashTable =
            this.groupEntityVersionsByEntityId(projectVersion);
        return VersionCalculator.calculateVersionEntitiesAtProjectVersion(projectVersion, entityHashTable);
    }

    @Override
    public Optional<VersionEntity> findVersionEntityByProjectVersionAndBaseEntityId(
        ProjectVersion projectVersion, UUID entityId) {
        Map<UUID, List<VersionEntity>> entityHashTable = createVersionEntityMap(projectVersion, List.of(entityId));
        return findVersionEntityByProjectVersionAndBaseEntityId(projectVersion, entityId, entityHashTable);
    }

    /**
     * Returns the version of the entity specified by entity id in given project version.
     *
     * @param projectVersion  The version of the entity to retrieve.
     * @param entityId        The id of the base entity whose version is being retrieved.
     * @param entityHashTable The map of entity ids to version entities. Used to speed up retrieval.
     *                        See {@link #createVersionEntityMap(ProjectVersion, List)}.
     * @return Optional of entity version at given project version.
     */
    public Optional<VersionEntity> findVersionEntityByProjectVersionAndBaseEntityId(
        ProjectVersion projectVersion, UUID entityId, Map<UUID, List<VersionEntity>> entityHashTable) {

        Map<UUID, List<VersionEntity>> justThisEntityMap = new HashMap<>();
        justThisEntityMap.put(entityId, entityHashTable.getOrDefault(entityId, List.of()));

        List<VersionEntity> currentVersionQuery = VersionCalculator.calculateVersionEntitiesAtProjectVersion(
            projectVersion, justThisEntityMap);
        return currentVersionQuery.isEmpty() ? Optional.empty() : Optional.of(currentVersionQuery.get(0));
    }

    @Override
    public Map<UUID, List<VersionEntity>> createVersionEntityMap(ProjectVersion projectVersion,
                                                                 List<UUID> baseEntityIds) {
        Map<UUID, List<VersionEntity>> entityHashTable = new HashMap<>();
        addToVersionEntityMap(entityHashTable, baseEntityIds);
        return entityHashTable;
    }

    private Map<UUID, List<VersionEntity>> addToVersionEntityMap(Map<UUID, List<VersionEntity>> entityHashTable,
                                                                 List<UUID> baseEntityIds) {
        baseEntityIds = baseEntityIds.stream().filter(i -> i != null).collect(Collectors.toList());
        this.retrieveVersionEntitiesByBaseIds(baseEntityIds)
            .forEach(versionEntity -> {
                if (entityHashTable.containsKey(versionEntity.getBaseEntityId())) {
                    entityHashTable.get(versionEntity.getBaseEntityId()).add(versionEntity);
                } else {
                    List<VersionEntity> versionEntities = new ArrayList<>();
                    versionEntities.add(versionEntity);
                    entityHashTable.put(versionEntity.getBaseEntityId(), versionEntities);
                }
            });
        Set<UUID> registeredIds = entityHashTable.keySet();
        if (!registeredIds.containsAll(baseEntityIds)) {
            List<UUID> missingIds = baseEntityIds.stream().filter(id -> !registeredIds.contains(id))
                .collect(Collectors.toList());
            throw new SafaError(String.format("Unable to find find all : %s", missingIds));
        }

        return entityHashTable;
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
    public Pair<VersionEntity, CommitError> commitAppEntityToProjectVersion(
        ProjectVersion projectVersion, AppEntity appEntity, SafaUser user,
        Map<UUID, List<VersionEntity>> entityHashTable) {

        VersionEntityAction<VersionEntity> versionEntityAction = () -> {
            BaseEntity baseEntity = this.createOrUpdateRelatedEntities(projectVersion, appEntity, user);

            VersionEntity versionEntity = this.instantiateVersionEntityFromAppEntity(
                projectVersion,
                baseEntity,
                appEntity);

            if (versionEntity.getModificationType() != ModificationType.NO_MODIFICATION) {
                createOrUpdateVersionEntity(versionEntity, user, entityHashTable);
                UUID baseEntityId = baseEntity.getBaseEntityId();
                appEntity.setId(baseEntityId);
            }

            return Optional.of(versionEntity);
        };
        UUID baseEntityId = appEntity.getId();
        return commitErrorHandler(projectVersion, versionEntityAction, baseEntityId, this.getProjectActivity());
    }

    @Override
    public Pair<VersionEntity, CommitError> deleteVersionEntityByBaseEntityId(
        ProjectVersion projectVersion, UUID baseEntityId, SafaUser user,
        Map<UUID, List<VersionEntity>> entityHashTable) {

        VersionEntityAction<VersionEntity> versionEntityAction = () -> {
            BaseEntity baseEntity = this.findBaseEntityById(baseEntityId).orElseThrow();
            VersionEntity removedVersionEntity = this.instantiateVersionEntityFromAppEntity(
                projectVersion,
                baseEntity,
                null); // null tells method that this is a deletion.
            this.createOrUpdateVersionEntity(removedVersionEntity, user, entityHashTable);
            return removedVersionEntity == null ? Optional.empty() : Optional.of(removedVersionEntity);
        };
        return commitErrorHandler(projectVersion, versionEntityAction, baseEntityId, this.getProjectActivity());
    }

    @Override
    public EntityDelta<AppEntity> calculateEntityDelta(
        ProjectVersion baselineVersion,
        ProjectVersion targetVersion) {
        Project project = baselineVersion.getProject();
        Map<UUID, AppEntity> addedEntities = new HashMap<>();
        Map<UUID, ModifiedEntity<AppEntity>> modifiedEntities = new HashMap<>();
        Map<UUID, AppEntity> removedEntities = new HashMap<>();

        List<BaseEntity> projectArtifacts = this.retrieveBaseEntitiesByProject(project);

        for (BaseEntity baseEntity : projectArtifacts) {
            Triplet<VersionEntity, VersionEntity, ModificationType> delta = this
                .calculateDeltaEntityBetweenProjectVersions(
                    baseEntity,
                    baselineVersion,
                    targetVersion);
            ModificationType modificationType = delta.getValue2();
            if (modificationType == null) {
                continue;
            }
            UUID baseEntityId = baseEntity.getBaseEntityId();

            switch (modificationType) {
                case ADDED:
                    AppEntity appEntity = this.retrieveAppEntityFromVersionEntity(delta.getValue1());
                    addedEntities.put(baseEntityId, appEntity);
                    break;
                case MODIFIED:
                    AppEntity appBefore = this.retrieveAppEntityFromVersionEntity(delta.getValue0());
                    AppEntity appAfter = this.retrieveAppEntityFromVersionEntity(delta.getValue1());
                    ModifiedEntity<AppEntity> modifiedEntity = new ModifiedEntity<>(appBefore, appAfter);
                    modifiedEntities.put(baseEntityId, modifiedEntity);
                    break;
                case REMOVED:
                    AppEntity appRemoved = this.retrieveAppEntityFromVersionEntity(delta.getValue0());
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
    public List<Pair<VersionEntity, CommitError>> commitAllAppEntitiesToProjectVersion(
        ProjectVersion projectVersion,
        List<AppEntity> appEntities,
        boolean asCompleteSet,
        SafaUser user) {

        List<UUID> processedAppEntities = new ArrayList<>();
        List<UUID> entityIds = appEntities
            .stream()
            .map(IAppEntity::getId)
            .filter(t -> t != null)
            .collect(Collectors.toList());
        Map<UUID, List<VersionEntity>> entityHashTable = createVersionEntityMap(projectVersion, entityIds);
        List<Pair<VersionEntity, CommitError>> response = appEntities
            .stream()
            .map(appEntity -> {
                Pair<VersionEntity, CommitError> commitResponse =
                    this.commitAppEntityToProjectVersion(projectVersion, appEntity, user, entityHashTable);
                if (commitResponse.getValue1() == null) {
                    UUID baseEntityId = commitResponse.getValue0().getBaseEntityId();
                    processedAppEntities.add(baseEntityId);
                    appEntity.setId(baseEntityId);
                }
                return commitResponse;
            })
            .collect(Collectors.toList());

        if (asCompleteSet) { // calculates deleted entities if this is complete set
            List<UUID> deletedBaseEntityIds = this.retrieveBaseEntitiesByProject(
                    projectVersion.getProject())
                .stream()
                .filter(baseEntity -> !processedAppEntities.contains(baseEntity.getBaseEntityId()))
                .map(BaseEntity::getBaseEntityId)
                .collect(Collectors.toList());

            addToVersionEntityMap(entityHashTable, deletedBaseEntityIds);

            List<Pair<VersionEntity, CommitError>> removedVersionEntities = deletedBaseEntityIds
                .stream()
                .map(baseEntityId -> this.deleteVersionEntityByBaseEntityId(projectVersion,
                    baseEntityId,
                    user,
                    entityHashTable))
                .collect(Collectors.toList());
            response.addAll(removedVersionEntities);
        }

        return response;
    }

    private void createOrUpdateVersionEntity(VersionEntity versionEntity, SafaUser user,
                                             Map<UUID, List<VersionEntity>> entityHashTable) throws SafaError {
        try {

            this.queryVersionEntity(versionEntity).ifPresent(existingVersionEntity ->
                versionEntity.setVersionEntityId(existingVersionEntity.getVersionEntityId()));

            Optional<VersionEntity> previousEntityOptional =
                findVersionEntityByProjectVersionAndBaseEntityId(versionEntity.getProjectVersion(),
                    versionEntity.getBaseEntityId(), entityHashTable);
            VersionEntity previousEntity = previousEntityOptional.orElse(null);

            this.save(versionEntity);

            this.updateTimInfo(versionEntity.getProjectVersion(), versionEntity, previousEntity, user);
        } catch (Exception e) {
            e.printStackTrace();
            UUID baseEntityId = versionEntity.getBaseEntityId();
            String error = String.format("An error occurred while saving version entity with base id: %s",
                baseEntityId);
            throw new SafaError(error, e);
        }
    }

    private Triplet<VersionEntity, VersionEntity, ModificationType> calculateDeltaEntityBetweenProjectVersions(
        BaseEntity baseEntity,
        ProjectVersion baseVersion,
        ProjectVersion targetVersion) {
        List<VersionEntity> bodies = this.retrieveVersionEntitiesByBaseEntity(baseEntity);

        VersionEntity beforeEntity = this.versionCalculator.getEntityAtVersion(bodies,
            baseVersion, IVersionEntity::getProjectVersion);
        VersionEntity afterEntity = this.versionCalculator.getEntityAtVersion(bodies,
            targetVersion, IVersionEntity::getProjectVersion);

        ModificationType modificationType = this
            .calculateModificationType(beforeEntity, afterEntity);
        return new Triplet<>(beforeEntity, afterEntity, modificationType);
    }

    private Pair<VersionEntity, CommitError> commitErrorHandler(ProjectVersion projectVersion,
                                                                VersionEntityAction<VersionEntity> versionEntityAction,
                                                                UUID entityName,
                                                                ProjectEntityType projectEntityType) {
        String errorDescription = null;
        VersionEntity versionEntity = null;
        CommitError commitError = null;
        try {
            Optional<VersionEntity> versionEntityOptional = versionEntityAction.action();
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
            commitError = new CommitError(projectVersion, errorDescription, projectEntityType);
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
    private ModificationType calculateModificationType(VersionEntity baseEntity,
                                                       VersionEntity targetEntity) {
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

    private Map<UUID, List<VersionEntity>> groupEntityVersionsByEntityId(ProjectVersion projectVersion) {
        List<VersionEntity> versionEntities = this.retrieveVersionEntitiesByProject(projectVersion.getProject());
        return ProjectDataStructures.createGroupLookup(versionEntities, IVersionEntity::getBaseEntityId);
    }

    private VersionEntity instantiateVersionEntityFromAppEntity(ProjectVersion projectVersion,
                                                                BaseEntity baseEntity,
                                                                AppEntity appEntity) throws JsonProcessingException {
        ModificationType modificationType = this
            .calculateModificationTypeForAppEntity(projectVersion, baseEntity, appEntity);

        return this.instantiateVersionEntityWithModification(
            projectVersion,
            modificationType,
            baseEntity,
            appEntity);
    }

    private ModificationType calculateModificationTypeForAppEntity(ProjectVersion projectVersion,
                                                                   BaseEntity baseEntity,
                                                                   AppEntity appEntity) {
        VersionEntity previousBody = versionCalculator
            .getEntityBeforeVersion(this.retrieveVersionEntitiesByBaseEntity(baseEntity),
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
     * @param entity The base entities whose versions are retrieved
     * @return List of versions associated with given base entities.
     */
    protected abstract List<VersionEntity> retrieveVersionEntitiesByBaseEntity(BaseEntity entity);

    /**
     * @param project The project whose entities are retrieved.
     * @return Returns list of base entities existing in project.
     */
    protected abstract List<BaseEntity> retrieveBaseEntitiesByProject(Project project);

    /**
     * @param baseEntityId The name of the base entity.
     * @return Returns the base entity in given project with given name.
     */
    protected abstract Optional<BaseEntity> findBaseEntityById(UUID baseEntityId);

    /**
     * Creates or updates any entities related to AppEntity and returns the corresponding base entity.
     *
     * @param projectVersion    The project version associated with given app entity.
     * @param artifactAppEntity The application entity whose sub entities are being created.
     * @param user              The user doing the operation
     * @return Returns the base entity associated with given app entity.
     */
    protected abstract BaseEntity createOrUpdateRelatedEntities(ProjectVersion projectVersion,
                                                                AppEntity artifactAppEntity, SafaUser user)
        throws SafaError;

    /**
     * Creates an entity version with content of app entity and containing
     * given modification type.
     *
     * @param projectVersion   The project version where version entity is created.
     * @param modificationType The type of change required to move from last commit to given app entity.
     * @param baseEntity       The base entity represented by app entity.
     * @param appEntity        The app entity whose content is being compared to previous commits.
     * @return The version entity for saving the app entity content to project version.
     */
    protected abstract VersionEntity instantiateVersionEntityWithModification(ProjectVersion projectVersion,
                                                                              ModificationType modificationType,
                                                                              BaseEntity baseEntity,
                                                                              AppEntity appEntity)
        throws JsonProcessingException;

    /**
     * Returns the type of project entity this version repository corresponds to.
     *
     * @return ProjectEntity associated with this repository.
     */
    protected abstract ProjectEntityType getProjectActivity();

    /**
     * Given a VersionEntity this methods returns an optional possibly containing the source entity this
     * corresponds with.
     *
     * @param versionEntity The version entity being saved.
     * @return Optional possibly containing existing version entity.
     */
    protected abstract Optional<VersionEntity> queryVersionEntity(VersionEntity versionEntity);
}
