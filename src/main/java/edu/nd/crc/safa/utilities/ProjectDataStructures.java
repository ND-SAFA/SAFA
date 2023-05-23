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
}
