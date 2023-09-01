package edu.nd.crc.safa.utilities;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;

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
}
