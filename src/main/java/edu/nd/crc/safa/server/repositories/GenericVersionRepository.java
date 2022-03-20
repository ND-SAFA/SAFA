package edu.nd.crc.safa.server.repositories;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.AppConstraints;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.EntityDelta;
import edu.nd.crc.safa.server.entities.app.IAppEntity;
import edu.nd.crc.safa.server.entities.app.ModifiedEntity;
import edu.nd.crc.safa.server.entities.db.CommitError;
import edu.nd.crc.safa.server.entities.db.IBaseEntity;
import edu.nd.crc.safa.server.entities.db.IVersionEntity;
import edu.nd.crc.safa.server.entities.db.ModificationType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.VersionAction;
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
    protected abstract List<VersionEntity> getVersionEntitiesByProject(Project project);

    /**
     * @param entity The base entities whose versions are retrieved
     * @return List of versions associated with given base entities.
     */
    protected abstract List<VersionEntity> getVersionEntitiesByBaseEntity(BaseEntity entity);

    /**
     * @param baseEntityId The name of the base entity.
     * @return Returns the base entity in given project with given name.
     */
    protected abstract Optional<BaseEntity> findBaseEntityById(String baseEntityId);

    /**
     * @param project The project whose entities are retrieved.
     * @return Returns list of base entities existing in project.
     */
    protected abstract List<BaseEntity> getBaseEntitiesByProject(Project project);

    /**
     * Finds base entity associated with given app entity if an entity exists.
     * Otherwise, creates the base entity along with any missing auxiliary objects.
     *
     * @param projectVersion    The project version associated with given app entity.
     * @param artifactAppEntity The application entity whose sub entities are being created.
     * @return Returns the base entity associated with given app entity.
     */
    protected abstract BaseEntity findOrCreateBaseEntitiesFromAppEntity(ProjectVersion projectVersion,
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
    protected abstract VersionEntity createEntityVersionWithModification(ProjectVersion projectVersion,
                                                                         ModificationType modificationType,
                                                                         BaseEntity baseEntity,
                                                                         AppEntity appEntity);

    /**
     * Creates the VersionEntity representing a deletion in a project version.
     *
     * @param projectVersion The project version associated with deletion.
     * @param baseEntity     The base entity being deleted.
     * @return The version entity representing the deletion.
     */
    protected abstract VersionEntity createRemovedVersionEntity(ProjectVersion projectVersion,
                                                                BaseEntity baseEntity);

    /**
     * Saves given artifact version to project version, deleting any previous entry
     * to the project version if it exists.
     *
     * @param projectVersion  The project version which the entity is being saved to.
     * @param artifactVersion The version entity being saved.
     * @throws SafaError Throws error if saving fails.
     */
    protected abstract void saveOrOverrideVersionEntity(ProjectVersion projectVersion,
                                                        VersionEntity artifactVersion) throws SafaError;


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
     * Commits the current state of app entity to given project version. Note,
     * if submitted to an non-current version changes are not propagated upstream.
     *
     * @param projectVersion The project version to save the changes to.
     * @param appEntity      The app entity whose state is saved.
     * @return String representing parser error if one occurred.
     */
    @Override
    public Pair<VersionEntity, CommitError> commitSingleEntityToProjectVersion(ProjectVersion projectVersion,
                                                                               AppEntity appEntity) {
        VersionAction<VersionEntity> versionAction = () -> {
            Pair<BaseEntity, VersionEntity> entities = this
                .createVersionEntityFromAppEntity(projectVersion, appEntity);
            VersionEntity artifactVersion = entities.getValue1();
            if (artifactVersion == null) {
                return Optional.empty();
            }
            saveOrOverrideVersionEntity(projectVersion, artifactVersion);
            return Optional.of(artifactVersion);
        };
        return commitErrorHandler(projectVersion, versionAction, appEntity.getId());
    }

    @Override
    public List<Pair<VersionEntity, CommitError>> commitAllEntitiesInProjectVersion(ProjectVersion projectVersion,
                                                                                    List<AppEntity> appEntities) {
        List<Pair<VersionEntity, CommitError>> versionEntityPayloads = this
            .calculateVersionEntitiesFromAppEntities(projectVersion, appEntities);
        return versionEntityPayloads
            .stream()
            .map(payload -> {
                VersionEntity versionEntity = payload.getValue0();
                VersionAction<VersionEntity> versionAction = () -> {
                    if (versionEntity != null) {
                        this.saveOrOverrideVersionEntity(projectVersion, versionEntity);
                        return Optional.of(versionEntity);
                    } else {
                        return Optional.empty();
                    }
                };
                return commitErrorHandler(projectVersion, versionAction);
            })
            .collect(Collectors.toList());
    }

    @Override
    public Pair<VersionEntity, CommitError> deleteVersionEntityByBaseEntityId(
        ProjectVersion projectVersion,
        String baseEntityId) {
        VersionAction<VersionEntity> versionAction = () -> {
            Optional<BaseEntity> baseEntityOptional = this.findBaseEntityById(baseEntityId);

            if (baseEntityOptional.isPresent()) {
                BaseEntity baseEntity = baseEntityOptional.get();
                VersionEntity removedVersionEntity = this.createRemovedVersionEntity(projectVersion, baseEntity);
                this.saveOrOverrideVersionEntity(projectVersion, removedVersionEntity);
                return Optional.of(removedVersionEntity);
            } else {
                return Optional.empty();
            }
        };
        return commitErrorHandler(projectVersion, versionAction);
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
                                                                VersionAction versionAction) {
        return commitErrorHandler(projectVersion, versionAction, "unknown");
    }

    private Pair<VersionEntity, CommitError> commitErrorHandler(ProjectVersion projectVersion,
                                                                VersionAction<VersionEntity> versionAction,
                                                                String entityName) {
        String errorDescription = null;
        VersionEntity versionEntity = null;
        CommitError commitError = null;
        try {
            Optional<VersionEntity> versionEntityOptional = versionAction.action();
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
            errorDescription = e.getMessage();
        }
        if (errorDescription != null) {
            commitError = new CommitError(projectVersion, errorDescription);
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

    private List<VersionEntity> retrieveEntitiesAtProjectVersion(
        ProjectVersion projectVersion,
        Hashtable<String, List<VersionEntity>> entityVersionsByName) {
        List<VersionEntity> entityVersionsAtProjectVersion = new ArrayList<>();

        for (String entityName : entityVersionsByName.keySet()) {
            List<VersionEntity> allEntityVersion = entityVersionsByName.get(entityName);
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
        List<VersionEntity> versionEntities = this.getVersionEntitiesByProject(projectVersion.getProject());
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

    private List<Pair<VersionEntity, CommitError>> calculateVersionEntitiesFromAppEntities(
        ProjectVersion projectVersion,
        List<AppEntity> appEntities) {

        List<String> processedAppEntities = new ArrayList<>();
        List<VersionEntity> updatedVersionEntities = new ArrayList<>();
        List<CommitError> commitErrors = new ArrayList<>();
        List<Pair<VersionEntity, CommitError>> response = new ArrayList<>();

        for (AppEntity appEntity : appEntities) {
            VersionAction<VersionEntity> versionAction = () -> {
                Pair<BaseEntity, VersionEntity> entities = this
                    .createVersionEntityFromAppEntity(projectVersion, appEntity);
                BaseEntity baseEntity = entities.getValue0();
                VersionEntity versionEntity = entities.getValue1();

                boolean hasChanged = versionEntity != null;
                if (hasChanged) {
                    updatedVersionEntities.add(versionEntity);
                }
                String entityId = baseEntity.getBaseEntityId();
                appEntity.setId(entityId);
                processedAppEntities.add(entityId);

                return versionEntity == null ? Optional.empty() : Optional.of(versionEntity);
            };
            Pair<VersionEntity, CommitError> commitResponse = commitErrorHandler(projectVersion, versionAction,
                appEntity.getId());
            response.add(commitResponse);
        }

        List<Pair<VersionEntity, CommitError>> removedArtifactBodies = this.getBaseEntitiesByProject(
                projectVersion.getProject())
            .stream()
            .filter(baseEntity -> !processedAppEntities.contains(baseEntity.getBaseEntityId()))
            .map(baseEntity -> this.calculateVersionEntityFromAppEntity(projectVersion, baseEntity, null))
            .filter(Objects::nonNull)
            .map(versionEntity -> new Pair<VersionEntity, CommitError>(versionEntity, null))
            .collect(Collectors.toList());

        response.addAll(removedArtifactBodies);
        return response;
    }

    private Pair<BaseEntity, VersionEntity> createVersionEntityFromAppEntity(
        ProjectVersion projectVersion,
        AppEntity appEntity) throws SafaError {

        BaseEntity baseEntity = this.findOrCreateBaseEntitiesFromAppEntity(
            projectVersion,
            appEntity);

        VersionEntity versionEntity = this.calculateVersionEntityFromAppEntity(
            projectVersion,
            baseEntity,
            appEntity);
        return new Pair<>(baseEntity, versionEntity);
    }

    private VersionEntity calculateVersionEntityFromAppEntity(ProjectVersion projectVersion,
                                                              BaseEntity baseEntity,
                                                              AppEntity appEntity) {
        ModificationType modificationType = this
            .calculateModificationTypeForAppEntity(projectVersion, baseEntity, appEntity);

        if (modificationType == null) {
            return null;
        }

        return this.createEntityVersionWithModification(
            projectVersion,
            modificationType,
            baseEntity,
            appEntity);
    }

    private ModificationType calculateModificationTypeForAppEntity(ProjectVersion projectVersion,
                                                                   BaseEntity baseEntity,
                                                                   AppEntity appEntity) {
        VersionEntity previousBody =
            getEntityBeforeVersion(this.getVersionEntitiesByBaseEntity(baseEntity), projectVersion);
        if (previousBody == null) {
            return appEntity == null ? null : ModificationType.ADDED;
        } else {
            if (appEntity == null) {
                boolean previouslyRemoved = previousBody.getModificationType() == ModificationType.REMOVED;
                return previouslyRemoved ? null : ModificationType.REMOVED;
            } else { // app entity is not null
                if (previousBody.getModificationType() == ModificationType.REMOVED) {
                    return ModificationType.ADDED;
                }
                boolean hasSameContent = previousBody.hasSameContent(appEntity);
                return hasSameContent ? null : ModificationType.MODIFIED;
            }
        }
    }
}
