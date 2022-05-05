package unit.jobs;

import static org.junit.jupiter.api.Assertions.assertThrows;

import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.api.jobs.JobType;
import edu.nd.crc.safa.server.entities.api.jobs.ProjectCreationWorker;
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
        ProjectCreationWorker projectCreationWorker = buildProjectCreationWorker();
        for (String stepName : JobSteps.getJobSteps(JobType.PROJECT_CREATION)) {
            projectCreationWorker.getMethodFromStep(stepName);
        }
    }

    @Test
    public void notYetImplemented() {
        assertThrows(RuntimeException.class, () -> {
            buildProjectCreationWorker().getMethodFromStep("no exist");
        });
    }

    private ProjectCreationWorker buildProjectCreationWorker() {
        return new ProjectCreationWorker(
            new Job(),
            new ProjectCommit()
        );
    }
}
