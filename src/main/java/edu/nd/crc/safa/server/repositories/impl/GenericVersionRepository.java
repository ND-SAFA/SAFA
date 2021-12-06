package edu.nd.crc.safa.server.repositories.impl;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.AppConstraints;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.IAppEntity;
import edu.nd.crc.safa.server.entities.app.IDeltaEntity;
import edu.nd.crc.safa.server.entities.db.IBaseEntity;
import edu.nd.crc.safa.server.entities.db.IVersionEntity;
import edu.nd.crc.safa.server.entities.db.ModificationType;
import edu.nd.crc.safa.server.entities.db.ParserError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.utilities.ProjectVersionFilter;

import org.javatuples.Pair;
import org.springframework.dao.DataIntegrityViolationException;

/**
 * Implements the generic logic for retrieving, creating, and modifying versioned entities.
 *
 * @param <VersionEntity> The versioned entity.
 */
public abstract class GenericVersionRepository<
    BaseEntity extends IBaseEntity,
    VersionEntity extends IVersionEntity<AppEntity>,
    AppEntity extends IAppEntity,
    DeltaEntity extends IDeltaEntity>
    implements IVersionRepository<BaseEntity, VersionEntity, AppEntity, DeltaEntity> {

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
     * @param project           The project associated with given app entity.
     * @param artifactAppEntity The application entity whose sub entities are being created.
     * @return Returns the base entity associated with given app entity.
     */
    abstract BaseEntity findOrCreateBaseEntityFromAppEntity(Project project,
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
     * Creates and populated delta entity using the modification type and given
     * source and target version entities.
     *
     * @param modificationType    The type of change between base and target entities
     * @param baseEntityName      The name of the base entity.
     * @param baseVersionEntity   The version entity representing the start of the delta.
     * @param targetVersionEntity The version entity representing the final state of the delta.
     * @return The populated delta artifacts with given modification.
     */
    abstract DeltaEntity createDeltaEntity(ModificationType modificationType,
                                           String baseEntityName,
                                           VersionEntity baseVersionEntity,
                                           VersionEntity targetVersionEntity);

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
        Hashtable<String, List<VersionEntity>> artifactBodyTable =
            this.groupEntityVersionsByEntityId(projectVersion);
        return this.retrieveEntitiesAtProjectVersion(projectVersion, artifactBodyTable);
    }

    @Override
    public void commitAppEntityToProjectVersion(ProjectVersion projectVersion, AppEntity appEntity)
        throws SafaError {
        VersionEntity artifactVersion = this
            .calculateEntityVersionAtProjectVersion(projectVersion, appEntity);
        if (artifactVersion == null) {
            return;
        }
        saveOrOverrideVersionEntity(projectVersion, artifactVersion);
    }

    @Override
    public List<ParserError> commitAppEntitiesToProjectVersion(ProjectVersion projectVersion,
                                                               List<AppEntity> appEntities) throws SafaError {
        Pair<List<VersionEntity>, List<ParserError>> response = this
            .calculateApplicationEntitiesAtVersion(projectVersion, appEntities);

        for (VersionEntity body : response.getValue0()) {
            this.saveOrOverrideVersionEntity(projectVersion, body);
        }
        return response.getValue1();
    }

    @Override
    public DeltaEntity calculateDeltaEntityBetweenProjectVersions(BaseEntity baseEntity,
                                                                  ProjectVersion baseVersion,
                                                                  ProjectVersion targetVersion) {
        String artifactName = baseEntity.getBaseEntityId();
        List<VersionEntity> bodies = this.findVersionEntitiesWithBaseEntity(baseEntity);

        VersionEntity beforeBody = this.getEntityAtVersion(bodies,
            baseVersion);
        VersionEntity afterBody = this.getEntityAtVersion(bodies,
            targetVersion);

        ModificationType modificationType = this
            .calculateModificationType(beforeBody, afterBody);

        if (modificationType == null) {
            return null;
        }

        return this.createDeltaEntity(modificationType, artifactName, beforeBody, afterBody);
    }

    @Override
    public void deleteVersionEntityByBaseName(
        ProjectVersion projectVersion,
        String baseEntityName) throws SafaError {

        Project project = projectVersion.getProject();
        Optional<BaseEntity> baseEntityOptional = this
            .findBaseEntityByName(project, baseEntityName);

        if (baseEntityOptional.isPresent()) {
            BaseEntity baseEntity = baseEntityOptional.get();
            VersionEntity removedVersionEntity = this.createRemovedVersionEntity(projectVersion, baseEntity);
            this.saveOrOverrideVersionEntity(projectVersion, removedVersionEntity);
        }
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
        Hashtable<String, List<VersionEntity>> artifactBodiesByArtifactName) {
        List<VersionEntity> artifacts = new ArrayList<>();
        for (String key : artifactBodiesByArtifactName.keySet()) {
            List<VersionEntity> bodyVersions = artifactBodiesByArtifactName.get(key);
            VersionEntity latest = null;
            for (VersionEntity body : bodyVersions) {
                if (body.getProjectVersion().isLessThanOrEqualTo(projectVersion)) {
                    if (latest == null || body.getProjectVersion().isGreaterThan(latest.getProjectVersion())) {
                        latest = body;
                    }
                }
            }

            if (latest != null && latest.getModificationType() != ModificationType.REMOVED) {
                artifacts.add(latest);
            }
        }
        return artifacts;
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

    private VersionEntity getEntityAtVersion(List<VersionEntity> bodies, ProjectVersion version) {
        return this
            .getLatestEntityVersionWithFilter(bodies, (target) -> target.isLessThanOrEqualTo(version));
    }

    private VersionEntity getEntityBeforeVersion(List<VersionEntity> bodies, ProjectVersion version) {
        return this.getLatestEntityVersionWithFilter(bodies, (target) -> target.isLessThan(version));
    }

    private Pair<List<VersionEntity>, List<ParserError>> calculateApplicationEntitiesAtVersion(
        ProjectVersion projectVersion,
        List<AppEntity> appEntities) {

        Hashtable<String, AppEntity> artifactsUpdated = new Hashtable<>();
        List<VersionEntity> updatedArtifactBodies = new ArrayList<>();
        List<ParserError> parserErrors = new ArrayList<>();
        for (AppEntity appEntity : appEntities) {
            artifactsUpdated.put(appEntity.getName(), appEntity);
            String errorDescription = null;
            try {
                VersionEntity artifactVersion = this
                    .calculateEntityVersionAtProjectVersion(projectVersion, appEntity);
                updatedArtifactBodies.add(artifactVersion);
            } catch (DataIntegrityViolationException e) {
                e.printStackTrace();
                errorDescription =
                    "Could not parse entity " + appEntity.getName() + ": " + AppConstraints.getConstraintError(e);
            } catch (Exception e) {
                errorDescription =
                    "Could not parse entity " + appEntity.getName() + ": " + e.getMessage();
            }

            if (errorDescription != null) {
                ParserError parserError = new ParserError(
                    projectVersion,
                    errorDescription);
                parserErrors.add(parserError);
            }
        }
        updatedArtifactBodies = updatedArtifactBodies
            .stream()
            .filter(Objects::nonNull)
            .collect(Collectors.toList());

        List<VersionEntity> removedArtifactBodies = this.getBaseEntitiesInProject(
                projectVersion.getProject())
            .stream()
            .filter(a -> !artifactsUpdated.containsKey(a.getBaseEntityId()))
            .map(a -> this.calculateEntityVersionAtProjectVersion(projectVersion, a, null))
            .filter(Objects::nonNull)
            .collect(Collectors.toList());

        List<VersionEntity> allArtifactBodies = new ArrayList<>(updatedArtifactBodies);
        allArtifactBodies.addAll(removedArtifactBodies);
        return new Pair<>(allArtifactBodies, parserErrors);
    }

    private VersionEntity calculateEntityVersionAtProjectVersion(ProjectVersion projectVersion,
                                                                 BaseEntity artifact,
                                                                 AppEntity appEntity) {
        ModificationType modificationType = this
            .calculateModificationTypeForAppEntity(projectVersion, artifact, appEntity);

        if (modificationType == null) {
            return null;
        }

        return this
            .createEntityVersionWithModification(
                projectVersion,
                modificationType,
                artifact,
                appEntity);

    }

    private VersionEntity calculateEntityVersionAtProjectVersion(
        ProjectVersion projectVersion,
        AppEntity appEntity) throws SafaError {

        BaseEntity baseEntity = this.findOrCreateBaseEntityFromAppEntity(
            projectVersion.getProject(),
            appEntity);

        return this.calculateEntityVersionAtProjectVersion(
            projectVersion,
            baseEntity,
            appEntity);
    }
}
