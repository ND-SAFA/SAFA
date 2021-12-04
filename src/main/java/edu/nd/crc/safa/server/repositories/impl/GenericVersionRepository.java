package edu.nd.crc.safa.server.repositories.impl;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;

import edu.nd.crc.safa.server.entities.app.IAppEntity;
import edu.nd.crc.safa.server.entities.db.IEntity;
import edu.nd.crc.safa.server.entities.db.IEntityVersion;
import edu.nd.crc.safa.server.entities.db.ModificationType;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.utilities.ProjectVersionFilter;

/**
 * Implements the generic logic for retrieving, creating, and modifying versioned entities.
 *
 * @param <VersionType> The versioned entity.
 */
public abstract class GenericVersionRepository<
    EntityType extends IEntity,
    VersionType extends IEntityVersion<AppType>,
    AppType extends IAppEntity>
    implements IVersionRepository<EntityType, VersionType, AppType> {


    /**
     * Calculates contents of each artifact at given version and returns bodies at version.
     *
     * @param projectVersion - The version of the artifact bodies that are returned
     * @return list of artifact bodies in project at given version
     */
    @Override
    public List<VersionType> getEntitiesAtVersion(ProjectVersion projectVersion) {
        Hashtable<String, List<VersionType>> artifactBodyTable =
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
    public VersionType getLatestEntityVersionWithFilter(List<VersionType> bodies,
                                                        ProjectVersionFilter filter) {
        VersionType closestBodyToVersion = null;
        for (int i = bodies.size() - 1; i >= 0; i--) {
            VersionType currentBody = bodies.get(i);
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
    public ModificationType calculateModificationType(VersionType baseEntity,
                                                      VersionType targetEntity) {
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

    private List<VersionType> retrieveEntitiesAtProjectVersion(
        ProjectVersion projectVersion,
        Hashtable<String, List<VersionType>> artifactBodiesByArtifactName) {
        List<VersionType> artifacts = new ArrayList<>();
        for (String key : artifactBodiesByArtifactName.keySet()) {
            List<VersionType> bodyVersions = artifactBodiesByArtifactName.get(key);
            VersionType latest = null;
            for (VersionType body : bodyVersions) {
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

    private Hashtable<String, List<VersionType>> groupEntityVersionsByEntityId(ProjectVersion projectVersion) {
        Hashtable<String, List<VersionType>> entityHashtable = new Hashtable<>();
        List<VersionType> entityVersions = this.getEntitiesInProject(projectVersion.getProject());
        for (VersionType entityVersion : entityVersions) {
            String entityId = entityVersion.getEntityId();
            if (entityHashtable.containsKey(entityId)) {
                entityHashtable.get(entityId).add(entityVersion);
            } else {
                List<VersionType> newList = new ArrayList<>();
                newList.add(entityVersion);
                entityHashtable.put(entityId, newList);
            }
        }
        return entityHashtable;
    }

    public ModificationType calculateModificationTypeForAppEntity(ProjectVersion projectVersion,
                                                                  EntityType baseEntity,
                                                                  AppType appEntity) {
        VersionType previousBody =
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
    public VersionType getEntityAtVersion(List<VersionType> bodies, ProjectVersion version) {
        return this
            .getLatestEntityVersionWithFilter(bodies, (target) -> target.isLessThanOrEqualTo(version));
    }

    @Override
    public VersionType getEntityBeforeVersion(List<VersionType> bodies, ProjectVersion version) {
        return this.getLatestEntityVersionWithFilter(bodies, (target) -> target.isLessThan(version));
    }
}
