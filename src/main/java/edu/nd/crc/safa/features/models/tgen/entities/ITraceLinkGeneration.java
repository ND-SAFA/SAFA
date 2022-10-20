package edu.nd.crc.safa.features.models.tgen.entities;

import java.util.List;

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
     * @param tracingRequests List of levels of artifacts containing sources and targets.
     * @return List of generated trace links.
     */
    List<TraceAppEntity> generateLinksWithState(String statePath,
                                                boolean loadFromStorage,
                                                TracingPayload tracingRequests);

    /**
     * Generates trace links between source and target artifacts used default state path.
     *
     * @param tracingRequests List of levels of artifacts containing sources and targets.
     * @return List of generated trace links.
     */
    List<TraceAppEntity> generateLinksWithBaselineState(TracingPayload tracingRequests);
}
