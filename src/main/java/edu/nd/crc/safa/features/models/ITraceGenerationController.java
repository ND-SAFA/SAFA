package edu.nd.crc.safa.features.models;

import java.util.List;

import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.features.tgen.api.TGenDataset;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

/**
 * Defines API for a trace link generation algorithm.
 */
public interface ITraceGenerationController {

    /**
     * Generates trace links between each source and target artifact pair.
     *
     * @param tracingRequests List of levels of artifacts containing sources and targets.
     * @param logger          The logger used to store trace logs.
     * @return List of generated trace links.
     */
    List<TraceAppEntity> generateLinks(TGenDataset tracingRequests, JobLogger logger);
}
