package unit.jobs;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;

import edu.nd.crc.safa.server.entities.api.JobType;
import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.api.ProjectCreationWorker;
import edu.nd.crc.safa.server.entities.app.JobSteps;
import edu.nd.crc.safa.server.entities.db.Job;
import edu.nd.crc.safa.server.services.EntityVersionService;
import edu.nd.crc.safa.server.services.JobService;
import edu.nd.crc.safa.server.services.NotificationService;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.ApplicationBaseTest;

/**
 * Responsible for testing that the generic job worker is parsing
 * step correctly.
 */
public class TestJobWorker extends ApplicationBaseTest {

    @Autowired
    JobService jobService;

    @Autowired
    EntityVersionService entityVersionService;

    @Autowired
    NotificationService notificationService;

    @Test
    public void testCreateProjectWorker() {
        ProjectCreationWorker projectCreationWorker = new ProjectCreationWorker(
            new Job(),
            new ProjectCommit(),
            jobService,
            notificationService,
            entityVersionService,
            appEntityRetrievalService
        );
        List<String> stepNames = projectCreationWorker.getStepNames();
        for (String stepName : JobSteps.getJobSteps(JobType.PROJECT_CREATION)) {
            assertThat(stepNames.contains(stepName)).isTrue();
        }
    }
}
