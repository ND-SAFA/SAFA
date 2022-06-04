package edu.nd.crc.safa.server.repositories;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import edu.nd.crc.safa.common.AppConstraints;
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

    /**
     * @param project The project whose entities are retrieved.
     * @return Returns all versions of the base entities in a project.
     */
    protected abstract List<VersionEntity> retrieveVersionEntitiesByProject(Project project);

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
    protected abstract Optional<BaseEntity> findBaseEntityById(String baseEntityId);

    /**
     * Creates or updates any entities related to AppEntity and returns the corresponding base entity.
     *
     * @param projectVersion    The project version associated with given app entity.
     * @param artifactAppEntity The application entity whose sub entities are being created.
     * @return Returns the base entity associated with given app entity.
     */
    protected abstract BaseEntity createOrUpdateRelatedEntities(ProjectVersion projectVersion,
                                                                AppEntity artifactAppEntity) throws SafaError;

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
                                                                              AppEntity appEntity);

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
    protected abstract Optional<VersionEntity> findExistingVersionEntity(VersionEntity versionEntity);

    protected abstract VersionEntity save(VersionEntity versionEntity);

    @Override
    public List<AppEntity> retrieveAppEntitiesByProjectVersion(ProjectVersion projectVersion) {
        List<VersionEntity> artifactBodies = this.retrieveVersionEntitiesByProjectVersion(projectVersion);
        List<AppEntity> artifacts = new ArrayList<>();
        for (VersionEntity artifactVersion : artifactBodies) {
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
    public List<VersionEntity> retrieveVersionEntitiesByProjectVersion(ProjectVersion projectVersion) {
        Hashtable<String, List<VersionEntity>> entityHashTable =
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
    public Optional<VersionEntity> findVersionEntityByProjectVersionAndBaseEntityId(
        ProjectVersion projectVersion,
        String entityId) {
        List<VersionEntity> versionEntities = this.retrieveVersionEntitiesByProject(projectVersion.getProject())
            .stream()
            .filter(versionEntity -> versionEntity.getBaseEntityId().equals(entityId))
            .collect(Collectors.toList());
        Hashtable<String, List<VersionEntity>> entityHashTable = new Hashtable<>();
        entityHashTable.put(entityId, versionEntities);
        List<VersionEntity> currentVersionQuery = this.calculateVersionEntitiesAtProjectVersion(projectVersion,
            entityHashTable);
        return currentVersionQuery.size() == 0 ? Optional.empty() : Optional.of(currentVersionQuery.get(0));
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
    public Pair<VersionEntity, CommitError> commitAppEntityToProjectVersion(ProjectVersion projectVersion,
                                                                            AppEntity appEntity) {
        VersionEntityAction<VersionEntity> versionEntityAction = () -> {
            BaseEntity baseEntity = this.createOrUpdateRelatedEntities(
                projectVersion,
                appEntity);

            VersionEntity versionEntity = this.instantiateVersionEntityFromAppEntity(
                projectVersion,
                baseEntity,
                appEntity);
            
            if (versionEntity.getModificationType() != ModificationType.NO_MODIFICATION) {
                createOrUpdateVersionEntity(versionEntity);
                String baseEntityId = baseEntity.getBaseEntityId();
                appEntity.setBaseEntityId(baseEntityId);
            }

            return Optional.of(versionEntity);
        };
        String baseEntityId = appEntity.getBaseEntityId();
        return commitErrorHandler(projectVersion, versionEntityAction, baseEntityId, this.getProjectActivity());
    }

    @Override
    public Pair<VersionEntity, CommitError> deleteVersionEntityByBaseEntityId(
        ProjectVersion projectVersion,
        String baseEntityId) {
        VersionEntityAction<VersionEntity> versionEntityAction = () -> {
            Optional<BaseEntity> baseEntityOptional = this.findBaseEntityById(baseEntityId);

            if (baseEntityOptional.isPresent()) {
                BaseEntity baseEntity = baseEntityOptional.get();
                VersionEntity removedVersionEntity = this.instantiateVersionEntityFromAppEntity(
                    projectVersion,
                    baseEntity,
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
    public EntityDelta<AppEntity> calculateEntityDelta(
        ProjectVersion baselineVersion,
        ProjectVersion targetVersion) {
        Project project = baselineVersion.getProject();
        Hashtable<String, AppEntity> addedEntities = new Hashtable<>();
        Hashtable<String, ModifiedEntity<AppEntity>> modifiedEntities = new Hashtable<>();
        Hashtable<String, AppEntity> removedEntities = new Hashtable<>();

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
            String baseEntityId = baseEntity.getBaseEntityId();

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
                    throw new RuntimeException("Missing case in switch for modification type:" + modificationType);
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
    public List<Pair<VersionEntity, CommitError>> commitAllAppEntitiesToProjectVersion(
        ProjectVersion projectVersion,
        List<AppEntity> appEntities) {

        List<String> processedAppEntities = new ArrayList<>();
        List<Pair<VersionEntity, CommitError>> response = new ArrayList<>();
        for (AppEntity appEntity : appEntities) {
            Pair<VersionEntity, CommitError> commitResponse = this.commitAppEntityToProjectVersion(projectVersion,
                appEntity);
            CommitError error = commitResponse.getValue1();
            VersionEntity entity = commitResponse.getValue0();
            if (entity != null) {
                processedAppEntities.add(entity.getBaseEntityId());
            }
        }

        List<Pair<VersionEntity, CommitError>> removedVersionEntities = this.retrieveBaseEntitiesByProject(
                projectVersion.getProject())
            .stream()
            .filter(baseEntity -> !processedAppEntities.contains(baseEntity.getBaseEntityId()))
            .map(baseEntity -> this.deleteVersionEntityByBaseEntityId(
                projectVersion,
                baseEntity.getBaseEntityId()))
            .collect(Collectors.toList());

        response.addAll(removedVersionEntities);

        return response;
    }

    private void createOrUpdateVersionEntity(VersionEntity versionEntity) throws SafaError {
        try {
            this.findExistingVersionEntity(versionEntity)
                .ifPresent((existingVersionEntity) -> {
                    versionEntity.setVersionEntityId(existingVersionEntity.getVersionEntityId());
                });
            this.save(versionEntity);
        } catch (Exception e) {
            String name = versionEntity.getBaseEntityId();
            String error = String.format("An error occurred while saving version entity with base id: %s", name);
            throw new SafaError(error, e);
        }
    }

    private Triplet<VersionEntity, VersionEntity, ModificationType> calculateDeltaEntityBetweenProjectVersions(
        BaseEntity baseEntity,
        ProjectVersion baseVersion,
        ProjectVersion targetVersion) {
        List<VersionEntity> bodies = this.retrieveVersionEntitiesByBaseEntity(baseEntity);

        VersionEntity beforeEntity = this.getEntityAtVersion(bodies,
            baseVersion);
        VersionEntity afterEntity = this.getEntityAtVersion(bodies,
            targetVersion);

        ModificationType modificationType = this
            .calculateModificationType(beforeEntity, afterEntity);
        return new Triplet<>(beforeEntity, afterEntity, modificationType);
    }

    private Pair<VersionEntity, CommitError> commitErrorHandler(ProjectVersion projectVersion,
                                                                VersionEntityAction<VersionEntity> versionEntityAction,
                                                                String entityName,
                                                                ProjectEntity projectEntity) {
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
    private VersionEntity getLatestEntityVersionWithFilter(List<VersionEntity> bodies,
                                                           ProjectVersionFilter filter) {
        VersionEntity closestBodyToVersion = null;
        for (int i = bodies.size() - 1; i >= 0; i--) {
            VersionEntity currentBody = bodies.get(i);
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

    /**
     * Calculates the current version of artifact noted by the entries in the given map.
     *
     * @param projectVersion         The version returns for each entity in map.
     * @param nameToVersionEntityMap Contains artifact names as keys and their associated version entities as values.
     * @return List of version entities as showing up in given project version.
     */
    private List<VersionEntity> calculateVersionEntitiesAtProjectVersion(
        ProjectVersion projectVersion,
        Hashtable<String, List<VersionEntity>> nameToVersionEntityMap) {
        List<VersionEntity> entityVersionsAtProjectVersion = new ArrayList<>();

        for (String entityName : nameToVersionEntityMap.keySet()) {
            List<VersionEntity> allEntityVersion = nameToVersionEntityMap.get(entityName);
            VersionEntity latest = null;
            for (VersionEntity body : allEntityVersion) {
                if (body.getProjectVersion().isLessThanOrEqualTo(projectVersion)) {
                    if (latest == null || body.getProjectVersion().isGreaterThan(latest.getProjectVersion())) {
                        latest = body;
                    }
                }
            }

            if (latest != null && latest.getModificationType() != ModificationType.REMOVED) {
                entityVersionsAtProjectVersion.add(latest);
            }
        }
        return entityVersionsAtProjectVersion;
    }

    private Hashtable<String, List<VersionEntity>> groupEntityVersionsByEntityId(ProjectVersion projectVersion) {
        Hashtable<String, List<VersionEntity>> entityHashtable = new Hashtable<>();
        List<VersionEntity> versionEntities = this.retrieveVersionEntitiesByProject(projectVersion.getProject());
        for (VersionEntity versionEntity : versionEntities) {
            String entityId = versionEntity.getBaseEntityId();
            if (entityHashtable.containsKey(entityId)) {
                entityHashtable.get(entityId).add(versionEntity);
            } else {
                List<VersionEntity> newList = new ArrayList<>();
                newList.add(versionEntity);
                entityHashtable.put(entityId, newList);
            }
        }
        return entityHashtable;
    }

    private VersionEntity getEntityAtVersion(List<VersionEntity> bodies, ProjectVersion version) {
        return this
            .getLatestEntityVersionWithFilter(bodies, (target) -> target.isLessThanOrEqualTo(version));
    }

    private VersionEntity getEntityBeforeVersion(List<VersionEntity> bodies, ProjectVersion version) {
        return this.getLatestEntityVersionWithFilter(bodies, (target) -> target.isLessThan(version));
    }

    private VersionEntity instantiateVersionEntityFromAppEntity(ProjectVersion projectVersion,
                                                                BaseEntity baseEntity,
                                                                AppEntity appEntity) {
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
        VersionEntity previousBody =
            getEntityBeforeVersion(this.retrieveVersionEntitiesByBaseEntity(baseEntity), projectVersion);
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
