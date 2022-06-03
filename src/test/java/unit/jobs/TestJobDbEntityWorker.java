package unit.jobs;

import static org.junit.jupiter.api.Assertions.assertThrows;

import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.api.jobs.JobType;
import edu.nd.crc.safa.server.entities.api.jobs.ProjectCreationWorker;
import edu.nd.crc.safa.server.entities.app.JobSteps;
import edu.nd.crc.safa.server.entities.db.JobDbEntity;
import edu.nd.crc.safa.server.services.ServiceProvider;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.ApplicationBaseTest;

/**
 * Responsible for testing that the generic job worker is parsing
 * step correctly.
 */
public class TestJobDbEntityWorker extends ApplicationBaseTest {

    @Autowired
    ServiceProvider serviceProvider;

    @Test
    public void testCreateProjectWorker() {
        ProjectCreationWorker projectCreationWorker = buildProjectCreationWorker();
        for (String stepName : JobSteps.getJobSteps(JobType.PROJECT_CREATION)) {
            projectCreationWorker.getMethodForStepByName(stepName);
        }
    }

    @Test
    public void notYetImplemented() {
        assertThrows(RuntimeException.class, () -> {
            buildProjectCreationWorker().getMethodForStepByName("no exist");
        });
    }

    private ProjectCreationWorker buildProjectCreationWorker() {
        return new ProjectCreationWorker(
            new JobDbEntity(),
            serviceProvider,
            new ProjectCommit()
        );
    }
}
