package edu.nd.crc.safa.server.repositories.impl;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.AppConstraints;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.IAppEntity;
import edu.nd.crc.safa.server.entities.db.IBaseEntity;
import edu.nd.crc.safa.server.entities.db.IVersionEntity;
import edu.nd.crc.safa.server.entities.db.ModificationType;
import edu.nd.crc.safa.server.entities.db.ParserError;
import edu.nd.crc.safa.server.entities.db.ProjectParsingActivities;
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
    AppEntity extends IAppEntity>
    implements IVersionRepository<BaseEntity, VersionEntity, AppEntity> {


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

    /**
     * Returns the most recent entity version that passes given filter
     *
     * @param bodies The bodies to filter through
     * @param filter The filter deciding whether an entity's version is valid.
     * @return The latest entity version passing given filter.
     */
    public VersionEntity getLatestEntityVersionWithFilter(List<VersionEntity> bodies,
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
    public ModificationType calculateModificationType(VersionEntity baseEntity,
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

    public ModificationType calculateModificationTypeForAppEntity(ProjectVersion projectVersion,
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

    @Override
    public VersionEntity getEntityAtVersion(List<VersionEntity> bodies, ProjectVersion version) {
        return this
            .getLatestEntityVersionWithFilter(bodies, (target) -> target.isLessThanOrEqualTo(version));
    }

    @Override
    public VersionEntity getEntityBeforeVersion(List<VersionEntity> bodies, ProjectVersion version) {
        return this.getLatestEntityVersionWithFilter(bodies, (target) -> target.isLessThan(version));
    }

    @Override
    public VersionEntity calculateEntityVersionAtProjectVersion(ProjectVersion projectVersion,
                                                                BaseEntity artifact,
                                                                AppEntity appEntity) {
        ModificationType modificationType = this
            .calculateModificationTypeForAppEntity(projectVersion, artifact, appEntity);

        if (modificationType == null) {
            return null;
        }

        VersionEntity artifactVersion = this
            .createEntityVersionWithModification(
                projectVersion,
                modificationType,
                artifact,
                appEntity);

        this
            .findEntityVersionInProjectVersion(projectVersion, artifact)
            .ifPresent(version -> artifactVersion.setEntityVersionId(version.getEntityVersionId()));
        return artifactVersion;
    }

    @Override
    public VersionEntity calculateEntityVersionAtProjectVersion(
        ProjectVersion projectVersion,
        AppEntity appEntity) {
        BaseEntity baseEntity = this.findOrCreateBaseEntityFromAppEntity(
            projectVersion,
            appEntity);

        return this.calculateEntityVersionAtProjectVersion(
            projectVersion,
            baseEntity,
            appEntity);
    }

    @Override
    public void setAppEntityAtProjectVersion(ProjectVersion projectVersion, AppEntity artifact)
        throws SafaError {
        VersionEntity artifactVersion = this
            .calculateEntityVersionAtProjectVersion(projectVersion, artifact);
        if (artifactVersion == null) {
            return;
        }
        saveVersionEntity(artifactVersion);
    }

    @Override
    public List<ParserError> setAppEntitiesAtProjectVersion(ProjectVersion projectVersion,
                                                            List<AppEntity> appEntities) throws SafaError {
        Pair<List<VersionEntity>, List<ParserError>> response = this
            .calculateApplicationEntitiesAtVersion(projectVersion, appEntities);

        for (VersionEntity body : response.getValue0()) {
            this.saveVersionEntity(body);
        }
        return response.getValue1();
    }

    @Override
    public Pair<List<VersionEntity>, List<ParserError>> calculateApplicationEntitiesAtVersion(
        ProjectVersion projectVersion,
        List<AppEntity> appEntities) {
        Hashtable<String, AppEntity> artifactsUpdated = new Hashtable<>();
        List<VersionEntity> updatedArtifactBodies = new ArrayList<>();
        List<ParserError> parserErrors = new ArrayList<>();
        for (AppEntity appEntity : appEntities) {
            artifactsUpdated.put(appEntity.getName(), appEntity);
            try {
                VersionEntity artifactVersion = this
                    .calculateEntityVersionAtProjectVersion(projectVersion, appEntity);
                updatedArtifactBodies.add(artifactVersion);
            } catch (DataIntegrityViolationException e) {
                ParserError parserError = new ParserError(
                    projectVersion,
                    "Could not parse artifact " + appEntity.getName() + ": " + AppConstraints.getConstraintError(e),
                    ProjectParsingActivities.PARSING_ARTIFACTS);
                parserErrors.add(parserError);
            }
        }
        updatedArtifactBodies = updatedArtifactBodies
            .stream()
            .filter(Objects::nonNull)
            .collect(Collectors.toList());

        List<VersionEntity> removedArtifactBodies = this.getProjectBaseEntities(
                projectVersion.getProject())
            .stream()
            .filter(a -> !artifactsUpdated.containsKey(a.getName()))
            .map(a -> this.calculateEntityVersionAtProjectVersion(projectVersion, a, null))
            .filter(Objects::nonNull)
            .collect(Collectors.toList());

        List<VersionEntity> allArtifactBodies = new ArrayList<>(updatedArtifactBodies);
        allArtifactBodies.addAll(removedArtifactBodies);
        return new Pair<>(allArtifactBodies, parserErrors);
    }
}
