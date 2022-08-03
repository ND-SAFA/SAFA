package unit.jobs;

import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.UUID;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.db.JobDbEntity;

import org.junit.jupiter.api.Test;

class FlatFileTestJobDeletion extends JobBaseFlatFileTest {

    @Test
    void testDeleteJob() throws Exception {
        // Create job deletion endpoint
        UUID jobId = createJobFromDefaultProject();
        JobDbEntity job = this.jobService.getJobById(jobId);
        String route = RouteBuilder
            .withRoute(AppRoutes.Jobs.deleteJob)
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
