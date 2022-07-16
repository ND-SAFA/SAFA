package unit.jobs;

import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.UUID;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.db.JobDbEntity;

import org.junit.jupiter.api.Test;

public class TestJobDeletion extends JobBaseTest {

    @Test
    public void testDeleteJob() throws Exception {
        // Create job deletion endpoint
        UUID jobId = createJobFromDefaultProject();
        JobDbEntity job = this.jobService.getJobById(jobId);
        String route = RouteBuilder
            .withRoute(AppRoutes.Jobs.deleteJob)
            .withJob(job)
            .buildEndpoint();

        // Send deletion request
        sendDelete(route, status().isOk());

        // VP - Verify that job got deleted
        assertThrows(SafaError.class, () -> {
            this.jobService.getJobById(jobId);
        });
    }
}
