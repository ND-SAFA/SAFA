package edu.nd.crc.safa.features.versions;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.function.Function;

import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.ProjectVersionFilter;

/**
 * Calculates the most-up-to-date versions of items.
 */
public class VersionCalculator {
    public <A> Map<UUID, List<A>> groupEntityVersionsByEntityId(List<A> versionEntities,
                                                                Function<A, UUID> idGetter) {
        Map<UUID, List<A>> entityHashtable = new HashMap<>();
        for (A versionEntity : versionEntities) {
            UUID entityId = idGetter.apply(versionEntity);
            if (entityHashtable.containsKey(entityId)) {
                entityHashtable.get(entityId).add(versionEntity);
            } else {
                List<A> newList = new ArrayList<>();
                newList.add(versionEntity);
                entityHashtable.put(entityId, newList);
            }
        }
        return entityHashtable;
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
     * @param bodies The bodies to filter through
     * @param filter The filter deciding whether an entity's version is valid.
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
