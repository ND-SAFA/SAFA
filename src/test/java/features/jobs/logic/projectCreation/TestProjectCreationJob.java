package features.jobs.logic.projectCreation;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.lang.reflect.Method;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.app.JobSteps;
import edu.nd.crc.safa.features.jobs.entities.app.JobType;
import edu.nd.crc.safa.features.jobs.entities.app.ProjectCreationJob;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;

import features.base.ApplicationBaseTest;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

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
