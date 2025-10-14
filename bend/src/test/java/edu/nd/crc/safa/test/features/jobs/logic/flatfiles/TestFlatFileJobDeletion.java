package edu.nd.crc.safa.test.features.jobs.logic.flatfiles;

import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.test.features.jobs.base.AbstractUpdateProjectViaFlatFileTestCommonRequests;
import edu.nd.crc.safa.test.requests.RouteBuilder;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.junit.jupiter.api.Test;

class TestFlatFileJobDeletion extends AbstractUpdateProjectViaFlatFileTestCommonRequests {

    @Test
    void testDeleteJob() throws Exception {
        // Create job deletion endpoint
        UUID jobId = updateProjectViaFlatFiles(ProjectPaths.Resources.Tests.DefaultProject.V1);
        JobDbEntity job = this.jobService.getJobById(jobId);
        String route = RouteBuilder
            .withRoute(AppRoutes.Jobs.Meta.DELETE_JOB)
            .withJob(job)
            .buildEndpoint();

        // Send deletion request
        SafaRequest.withRoute(route).deleteWithJsonObject();

        // VP - Verify that job got deleted
        assertThrows(SafaError.class, () -> {
            this.jobService.getJobById(jobId);
        });
    }
}
