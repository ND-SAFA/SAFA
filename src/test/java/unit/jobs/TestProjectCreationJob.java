package unit.jobs;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.lang.reflect.Method;

import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.api.jobs.JobType;
import edu.nd.crc.safa.server.entities.api.jobs.ProjectCreationJob;
import edu.nd.crc.safa.server.entities.app.JobSteps;
import edu.nd.crc.safa.server.entities.db.JobDbEntity;
import edu.nd.crc.safa.server.services.ServiceProvider;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.ApplicationBaseTest;

/**
 * Tests that the generic job worker is parsing step correctly.
 */
class TestProjectCreationJob extends ApplicationBaseTest {

    @Autowired
    ServiceProvider serviceProvider;

    @Test
    void testThatStepsAreRetrieved() {
        ProjectCreationJob projectCreationJob = buildProjectCreationJob();
        for (String stepName : JobSteps.getJobSteps(JobType.PROJECT_CREATION)) {
            Method method = projectCreationJob.getMethodForStepByName(stepName);
            assertThat(method).isNotNull();
        }
    }

    @Test
    void testErrorThrownOnMethodNotFound() {
        assertThrows(RuntimeException.class, () -> {
            buildProjectCreationJob().getMethodForStepByName("no exist");
        });
    }

    private ProjectCreationJob buildProjectCreationJob() {
        return new ProjectCreationJob(
            new JobDbEntity(),
            serviceProvider,
            new ProjectCommit()
        );
    }
}
