package edu.nd.crc.safa.utilities;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.function.Function;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;

/**
 * Contains data structures for accessing project data.
 */
public class ProjectDataStructures {
    /**
     * Create map from artifact id (as UUID) to artifact.
     *
     * @param artifacts The artifact to include in map.
     * @return Map of artifacts.
     */
    public static Map<UUID, ArtifactAppEntity> createArtifactMap(List<ArtifactAppEntity> artifacts) {
        Map<UUID, ArtifactAppEntity> artifactMap = new HashMap<>();
        artifacts.forEach(a -> artifactMap.put(a.getId(), a));
        return artifactMap;
    }

    /**
     * Create map from artifact name to artifact.
     *
     * @param artifacts The artifact to include in map.
     * @return Map of artifacts.
     */
    public static Map<String, ArtifactAppEntity> createArtifactNameMap(List<ArtifactAppEntity> artifacts) {
        Map<String, ArtifactAppEntity> artifactMap = new HashMap<>();
        artifacts.forEach(a -> artifactMap.put(a.getName(), a));
        return artifactMap;
    }

    /**
     * Creates map of artifact to tracing content.
     *
     * @param artifacts List of artifacts to include in layer.
     * @return Map of artifact id to content.
     */
    public static Map<String, String> createArtifactLayer(List<ArtifactAppEntity> artifacts) {
        Map<String, String> artifactMap = new HashMap<>();
        artifacts
            .stream()
            .filter(a -> a.getTraceString().length() > 0)
            .forEach(a -> artifactMap.put(a.getName(), a.getTraceString()));
        return artifactMap;
    }

    /**
     * Groups given entities by the property defined by getter.
     *
     * @param versionEntities The list of entities to group.
     * @param idGetter        The function to determine the property for each entity.
     * @param <A>             The type of entity being grouped.
     * @param <P>             The type of property to group by.
     * @return Map of
     */
    public static <A, P> Map<P, List<A>> createGroupLookup(Iterable<A> versionEntities,
                                                           Function<A, P> idGetter) {
        Map<P, List<A>> entityHashtable = new HashMap<>();
        for (A versionEntity : versionEntities) {
            P entityId = idGetter.apply(versionEntity);
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

    /**
     * Groups given entities by the property defined by getter.
     *
     * @param versionEntities The list of entities to group.
     * @param idGetter        The function to determine the property for each entity.
     * @param <A>             The type of entity being grouped.
     * @param <P>             The type of property to group by.
     * @return Map of
     */
    public static <A, P> Map<P, A> createEntityLookup(List<A> versionEntities,
                                                      Function<A, P> idGetter) {
        Map<P, A> entityHashtable = new HashMap<>();
        for (A versionEntity : versionEntities) {
            P entityId = idGetter.apply(versionEntity);
            if (entityHashtable.containsKey(entityId)) {
                throw new SafaError(String.format("Multiple items found to single ID %s", entityId));
            } else {
                List<A> newList = new ArrayList<>();
                newList.add(versionEntity);
                entityHashtable.put(entityId, versionEntity);
            }
        }
        return entityHashtable;
    }
}
