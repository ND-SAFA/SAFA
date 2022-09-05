package edu.nd.crc.safa.features.tgen.entities;

import java.util.List;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

/**
 * Defines API for a trace link generation algorithm.
 */
public interface ITraceLinkGeneration {

    /**
     * Generates trace links between each source and target artifact pair.
     *
     * @param sourceArtifacts List of source artifacts.
     * @param targetArtifacts List o target artifacts.
     * @return List of generated trace links.
     */
    List<TraceAppEntity> generateLinks(List<ArtifactAppEntity> sourceArtifacts,
                                       List<ArtifactAppEntity> targetArtifacts);
}
