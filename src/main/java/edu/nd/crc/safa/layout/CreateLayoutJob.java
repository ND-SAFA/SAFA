package edu.nd.crc.safa.layout;

import java.util.List;

import edu.nd.crc.safa.server.entities.api.jobs.JobWorker;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.JobDbEntity;
import edu.nd.crc.safa.server.services.ServiceProvider;

/**
 * TODO: Define steps
 * TODO: Merge with KlayLayoutGenerator
 */
public class CreateLayoutJob extends JobWorker {
    List<ArtifactAppEntity> artifacts;
    List<TraceAppEntity> traces;

    public CreateLayoutJob(JobDbEntity jobDbEntity,
                           ServiceProvider serviceProvider,
                           List<ArtifactAppEntity> artifacts,
                           List<TraceAppEntity> traces) {
        super(jobDbEntity, serviceProvider);
        this.artifacts = artifacts;
        this.traces = traces;
    }
}
