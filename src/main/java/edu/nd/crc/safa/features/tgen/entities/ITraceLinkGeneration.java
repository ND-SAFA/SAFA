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
     * @param statePath       Path to the state of model.
     * @param loadFromStorage Whether statePath reference cloud storage.
     * @param sourceArtifacts List of source artifacts.
     * @param targetArtifacts List o target artifacts.
     * @return List of generated trace links.
     */
    List<TraceAppEntity> generateLinksWithState(String statePath,
                                                boolean loadFromStorage,
                                                List<ArtifactAppEntity> sourceArtifacts,
                                                List<ArtifactAppEntity> targetArtifacts);

    /**
     * Generates trace links between source and target artifacts used default state path.
     *
     * @param sourceArtifacts List of source artifacts.
     * @param targetArtifacts List of target artifacts.
     * @return List of generated trace links.
     */
    List<TraceAppEntity> generateLinksWithBaselineState(List<ArtifactAppEntity> sourceArtifacts,
                                                        List<ArtifactAppEntity> targetArtifacts);
}
