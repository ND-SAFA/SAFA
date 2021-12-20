package edu.nd.crc.safa.server.repositories.impl;

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
     * @return Queries for all version entities in given project.
     */
    abstract List<VersionEntity> getEntitiesInProject(Project project);

    /**
     * @param entity The base entities whose versions are retrieved
     * @return List of versions associated with given base entities.
     */
    abstract List<VersionEntity> findByEntity(BaseEntity entity);

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
    abstract VersionEntity createEntityVersionWithModification(ProjectVersion projectVersion,
                                                               ModificationType modificationType,
                                                               BaseEntity baseEntity,
                                                               AppEntity appEntity);

    /**
     * @param project The project to search for base entity.
     * @param name    The name of the base entity.
     * @return Returns the base entity in given project with given name.
     */
    abstract Optional<BaseEntity> findBaseEntityByName(Project project, String name);

    /**
     * Creates and missing auxiliary types used in app entity.
     *
     * @param projectVersion    The project version associated with given app entity.
     * @param artifactAppEntity The application entity whose sub entities are being created.
     * @return Returns the base entity associated with given app entity.
     */
    abstract BaseEntity findOrCreateBaseEntityFromAppEntity(ProjectVersion projectVersion,
                                                            AppEntity artifactAppEntity) throws SafaError;

    /**
     * Saves given artifact version to project version, deleting any previous entry
     * to the project version if it exists.
     *
     * @param projectVersion  The project version which the entity is being saved to.
     * @param artifactVersion The version entity being saved.
     * @throws SafaError Throws error if saving fails.
     */
    abstract void saveOrOverrideVersionEntity(ProjectVersion projectVersion,
                                              VersionEntity artifactVersion) throws SafaError;

    /**
     * @param project The project whose entities are retrieved.
     * @return Returns list of base entities existing in project.
     */
    abstract List<BaseEntity> getBaseEntitiesInProject(Project project);

    /**
     * Creates the VersionEntity representing a deletion in a project version.
     *
     * @param projectVersion The project version associated with deletion.
     * @param baseEntity     The base entity being deleted.
     * @return The version entity representing the deletion.
     */
    abstract VersionEntity createRemovedVersionEntity(ProjectVersion projectVersion,
                                                      BaseEntity baseEntity);

    /**
     * @param baseEntity The base entity whose versions are returned.
     * @return Returns list of versions associated with base entity.
     */
    abstract List<VersionEntity> findVersionEntitiesWithBaseEntity(BaseEntity baseEntity);

    /**
     * Calculates contents of each artifact at given version and returns bodies at version.
     *
     * @param projectVersion - The version of the artifact bodies that are returned
     * @return list of artifact bodies in project at given version
     */
    @Override
    public List<VersionEntity> getEntityVersionsInProjectVersion(ProjectVersion projectVersion) {
        Hashtable<String, List<VersionEntity>> entityHashTable =
            this.groupEntityVersionsByEntityId(projectVersion);
        return this.retrieveEntitiesAtProjectVersion(projectVersion, entityHashTable);
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
    public CommitError commitSingleEntityToProjectVersion(ProjectVersion projectVersion, AppEntity appEntity) {
        return commitErrorHandler(projectVersion, () -> {
            VersionEntity artifactVersion = this
                .calculateVersionEntityFromAppEntity(projectVersion, appEntity);
            if (artifactVersion == null) {
                return;
            }
            saveOrOverrideVersionEntity(projectVersion, artifactVersion);
        }, appEntity.getName());
    }

    @Override
    public List<CommitError> commitAllEntitiesInProjectVersion(ProjectVersion projectVersion,
                                                               List<AppEntity> appEntities) throws SafaError {
        Pair<List<VersionEntity>, List<CommitError>> response = this
            .calculateVersionEntitiesFromAppEntities(projectVersion, appEntities);
        List<CommitError> errors = response.getValue1();
        for (VersionEntity body : response.getValue0()) {
            CommitError error = commitErrorHandler(projectVersion, () -> {
                this.saveOrOverrideVersionEntity(projectVersion, body);
            });
            errors.add(error);
        }
        return errors.stream().filter(Objects::nonNull).collect(Collectors.toList());
    }

    @Override
    public CommitError deleteVersionEntityByBaseName(
        ProjectVersion projectVersion,
        String baseEntityName) {
        return commitErrorHandler(projectVersion,
            () -> {
                Project project = projectVersion.getProject();
                Optional<BaseEntity> baseEntityOptional = this
                    .findBaseEntityByName(project, baseEntityName);

                if (baseEntityOptional.isPresent()) {
                    BaseEntity baseEntity = baseEntityOptional.get();
                    VersionEntity removedVersionEntity = this.createRemovedVersionEntity(projectVersion, baseEntity);
                    this.saveOrOverrideVersionEntity(projectVersion, removedVersionEntity);
                }
            });
    }

    @Override
    public EntityDelta<AppEntity> calculateEntityDelta(
        ProjectVersion baselineVersion,
        ProjectVersion targetVersion) {
        Project project = baselineVersion.getProject();
        Hashtable<String, AppEntity> addedArtifacts = new Hashtable<>();
        Hashtable<String, ModifiedEntity<AppEntity>> modifiedArtifacts = new Hashtable<>();
        Hashtable<String, AppEntity> removedArtifacts = new Hashtable<>();

        List<BaseEntity> projectArtifacts = this.getBaseEntitiesInProject(project);

        for (BaseEntity artifact : projectArtifacts) {
            Triplet<VersionEntity, VersionEntity, ModificationType> delta = this
                .calculateDeltaEntityBetweenProjectVersions(
                    artifact,
                    baselineVersion,
                    targetVersion);
            ModificationType modificationType = delta.getValue2();
            if (modificationType == null) {
                continue;
            }
            String baseName = artifact.getBaseEntityId();

            switch (modificationType) {
                case ADDED:
                    AppEntity appEntity = this.createAppFromVersion(delta.getValue1());
                    addedArtifacts.put(baseName, appEntity);
                    break;
                case MODIFIED:
                    AppEntity appBefore = this.createAppFromVersion(delta.getValue0());
                    AppEntity appAfter = this.createAppFromVersion(delta.getValue1());
                    ModifiedEntity<AppEntity> modifiedEntity = new ModifiedEntity<>(appBefore, appAfter);
                    modifiedArtifacts.put(baseName, modifiedEntity);
                    break;
                case REMOVED:
                    AppEntity appRemoved = this.createAppFromVersion(delta.getValue0());
                    removedArtifacts.put(baseName, appRemoved);
                    break;
                default:
                    throw new RuntimeException("Missing case in switch for modification type:" + modificationType);
            }
        }

        return new EntityDelta<>(addedArtifacts, modifiedArtifacts, removedArtifacts);
    }

    private Triplet<VersionEntity, VersionEntity, ModificationType> calculateDeltaEntityBetweenProjectVersions(
        BaseEntity baseEntity,
        ProjectVersion baseVersion,
        ProjectVersion targetVersion) {
        List<VersionEntity> bodies = this.findVersionEntitiesWithBaseEntity(baseEntity);

        VersionEntity beforeEntity = this.getEntityAtVersion(bodies,
            baseVersion);
        VersionEntity afterEntity = this.getEntityAtVersion(bodies,
            targetVersion);

        ModificationType modificationType = this
            .calculateModificationType(beforeEntity, afterEntity);

        return new Triplet<>(beforeEntity, afterEntity, modificationType);
    }

    private CommitError commitErrorHandler(ProjectVersion projectVersion,
                                           VersionAction versionAction) {
        return commitErrorHandler(projectVersion, versionAction, "unknown");
    }

    private CommitError commitErrorHandler(ProjectVersion projectVersion,
                                           VersionAction versionAction,
                                           String entityName) {
        String errorDescription = null;
        try {
            versionAction.action();
            return null;
        } catch (DataIntegrityViolationException e) {
            e.printStackTrace();
            errorDescription =
                "Could not parse entity " + entityName + ": " + AppConstraints.getConstraintError(e);
        } catch (Exception e) {
            errorDescription = e.getMessage();
        }
        if (errorDescription != null) {
            return new CommitError(projectVersion, errorDescription);
        }
        return null;
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
        List<VersionEntity> versionEntities = new ArrayList<>();
        for (String entityName : entityVersionsByName.keySet()) {
            List<VersionEntity> entityVersions = entityVersionsByName.get(entityName);
            VersionEntity latest = null;
            for (VersionEntity body : entityVersions) {
                if (body.getProjectVersion().isLessThanOrEqualTo(projectVersion)) {
                    if (latest == null || body.getProjectVersion().isGreaterThan(latest.getProjectVersion())) {
                        latest = body;
                    }
                }
            }

            if (latest != null && latest.getModificationType() != ModificationType.REMOVED) {
                versionEntities.add(latest);
            }
        }
        return versionEntities;
    }

    private Hashtable<String, List<VersionEntity>> groupEntityVersionsByEntityId(ProjectVersion projectVersion) {
        Hashtable<String, List<VersionEntity>> entityHashtable = new Hashtable<>();
        List<VersionEntity> versionEntities = this.getEntitiesInProject(projectVersion.getProject());
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

    private Pair<List<VersionEntity>, List<CommitError>> calculateVersionEntitiesFromAppEntities(
        ProjectVersion projectVersion,
        List<AppEntity> appEntities) {

        Hashtable<String, AppEntity> updatedAppEntities = new Hashtable<>();
        List<VersionEntity> updatedVersionEntities = new ArrayList<>();
        List<CommitError> commitErrors = new ArrayList<>();

        for (AppEntity appEntity : appEntities) {
            CommitError commitError = commitErrorHandler(projectVersion, () -> {
                VersionEntity artifactVersion = this
                    .calculateVersionEntityFromAppEntity(projectVersion, appEntity);
                if (artifactVersion != null) {
                    updatedVersionEntities.add(artifactVersion);
                }
                updatedAppEntities.put(appEntity.getName(), appEntity);
            }, appEntity.getName());
            commitErrors.add(commitError);
        }

        List<VersionEntity> removedArtifactBodies = this.getBaseEntitiesInProject(
                projectVersion.getProject())
            .stream()
            .filter(a -> !updatedAppEntities.containsKey(a.getBaseEntityId()))
            .map(a -> this.calculateVersionEntityFromAppEntity(projectVersion, a, null))
            .filter(Objects::nonNull)
            .collect(Collectors.toList());

        List<VersionEntity> allArtifactBodies = new ArrayList<>(updatedVersionEntities);
        allArtifactBodies.addAll(removedArtifactBodies);
        return new Pair<>(allArtifactBodies, commitErrors);
    }

    private VersionEntity calculateVersionEntityFromAppEntity(
        ProjectVersion projectVersion,
        AppEntity appEntity) throws SafaError {

        BaseEntity baseEntity = this.findOrCreateBaseEntityFromAppEntity(
            projectVersion,
            appEntity);

        return this.calculateVersionEntityFromAppEntity(
            projectVersion,
            baseEntity,
            appEntity);
    }

    private VersionEntity calculateVersionEntityFromAppEntity(ProjectVersion projectVersion,
                                                              BaseEntity artifact,
                                                              AppEntity appEntity) {
        ModificationType modificationType = this
            .calculateModificationTypeForAppEntity(projectVersion, artifact, appEntity);

        if (modificationType == null) {
            return null;
        }

        return this.createEntityVersionWithModification(
            projectVersion,
            modificationType,
            artifact,
            appEntity);

    }

    private ModificationType calculateModificationTypeForAppEntity(ProjectVersion projectVersion,
                                                                   BaseEntity baseEntity,
                                                                   AppEntity appEntity) {
        VersionEntity previousBody =
            getEntityBeforeVersion(this.findByEntity(baseEntity), projectVersion);

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
