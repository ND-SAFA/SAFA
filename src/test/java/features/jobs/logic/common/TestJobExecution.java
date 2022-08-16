package features.jobs.logic.common;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.io.IOException;
import java.lang.reflect.Method;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.app.CommitJob;
import edu.nd.crc.safa.features.jobs.entities.app.JobSteps;
import edu.nd.crc.safa.features.jobs.entities.app.JobType;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import features.base.ApplicationBaseTest;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Tests that the generic job worker is parsing step correctly.
 */
class TestJobExecution extends ApplicationBaseTest {

    @Autowired
    ServiceProvider serviceProvider;
    ProjectVersion projectVersion;

    @BeforeEach
    public void createProject() throws IOException {
        this.projectVersion = setupTestService.createDefaultProject("project");
    }

    @Test
    void testThatStepsAreRetrieved() throws IOException {
        CommitJob commitJob = buildProjectCreationJob();
        for (String stepName : JobSteps.getJobSteps(JobType.PROJECT_CREATION)) {
            Method method = commitJob.getMethodForStepByName(stepName);
            assertThat(method).isNotNull();
        }
    }

    @Test
    void testErrorThrownOnMethodNotFound() {
        assertThrows(RuntimeException.class, () -> {
            buildProjectCreationJob().getMethodForStepByName("no exist");
        });
    }

    private CommitJob buildProjectCreationJob() {
        return new CommitJob(
            new JobDbEntity(),
            serviceProvider,
            new ProjectCommit(projectVersion, false)
        );
    }
}
