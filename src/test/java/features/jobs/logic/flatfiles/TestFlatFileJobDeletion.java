package features.jobs.logic.flatfiles;

import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.UUID;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import features.jobs.base.AbstractUpdateProjectViaFlatFileTest;
import org.junit.jupiter.api.Test;

class TestFlatFileJobDeletion extends AbstractUpdateProjectViaFlatFileTest {

    @Test
    void testDeleteJob() throws Exception {
        // Create job deletion endpoint
        UUID jobId = updateProjectViaFlatFiles(ProjectPaths.Tests.DefaultProject.V1);
        JobDbEntity job = this.jobService.getJobById(jobId);
        String route = RouteBuilder
            .withRoute(AppRoutes.Jobs.DELETE_JOB)
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
