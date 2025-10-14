package edu.nd.crc.safa.features.versions;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.function.Function;

import edu.nd.crc.safa.features.common.IVersionEntity;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.ProjectDataStructures;
import edu.nd.crc.safa.utilities.ProjectVersionFilter;

/**
 * Calculates the most-up-to-date versions of items.
 */
public class VersionCalculator {

    public static <V extends IVersionEntity> List<V> getEntitiesAtVersion(ProjectVersion projectVersion,
                                                                          List<V> versionEntities) {
        Map<UUID, List<V>> entityMap = ProjectDataStructures.createGroupLookup(versionEntities,
            IVersionEntity::getBaseEntityId);
        return calculateVersionEntitiesAtProjectVersion(projectVersion, entityMap);
    }

    /**
     * Calculates the current version of artifact noted by the entries in the given map.
     *
     * @param projectVersion         The version returns for each entity in map.
     * @param nameToVersionEntityMap Contains artifact names as keys and their associated version entities as values.
     * @param <V>                    The version entity to return.
     * @return List of version entities as showing up in given project version.
     */
    public static <V extends IVersionEntity> List<V> calculateVersionEntitiesAtProjectVersion(
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

    public <V> V getEntityAtVersion(List<V> bodies,
                                    ProjectVersion version,
                                    Function<V, ProjectVersion> projectVersionFunction
    ) {
        return this
            .getLatestEntityVersionWithFilter(bodies,
                target -> target.isLessThanOrEqualTo(version),
                projectVersionFunction);
    }

    public <V> V getEntityBeforeVersion(List<V> bodies,
                                        ProjectVersion version,
                                        Function<V, ProjectVersion> projectVersionFunction
    ) {
        return this.getLatestEntityVersionWithFilter(bodies,
            target -> target.isLessThan(version),
            projectVersionFunction);
    }

    /**
     * Returns the most recent entity version that passes given filter
     *
     * @param bodies                 The bodies to filter through
     * @param filter                 The filter deciding whether an entity's version is valid.
     * @param projectVersionFunction Function to extract project version from generic entity V.
     * @param <V>                    The type of entity with some version to return from.
     * @return The latest entity version passing given filter.
     */
    public <V> V getLatestEntityVersionWithFilter(List<V> bodies,
                                                  ProjectVersionFilter filter,
                                                  Function<V, ProjectVersion> projectVersionFunction) {
        V closestItem = null;
        for (int i = bodies.size() - 1; i >= 0; i--) {
            V currentBody = bodies.get(i);
            ProjectVersion currentBodyVersion = projectVersionFunction.apply(currentBody);
            if (filter.shouldKeep(currentBodyVersion)) {
                if (closestItem == null) {
                    closestItem = currentBody;
                } else if (currentBodyVersion.isGreaterThan(projectVersionFunction.apply(closestItem))
                ) {
                    closestItem = currentBody;
                }
            }
        }
        return closestItem;
    }
}
