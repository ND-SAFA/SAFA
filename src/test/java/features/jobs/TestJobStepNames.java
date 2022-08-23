package features.jobs;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;

import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.app.JobSteps;
import edu.nd.crc.safa.features.jobs.entities.app.JobType;

import features.base.ApplicationBaseTest;
import org.junit.jupiter.api.Test;

/**
 * Tests that the correct steps are retrieved for each available job.
 */
public class TestJobStepNames extends ApplicationBaseTest {
    @Test
    public void negativeIndices() {
        assertThat(AbstractJob.getStepIndex(-1, 1)).isEqualTo(0);
        assertThat(AbstractJob.getStepIndex(-2, 5)).isEqualTo(3);
    }

    @Test
    public void testCommitJobSteps() {
        List<String> stepNames = JobSteps.getJobSteps(JobType.PROJECT_CREATION);
        assertThat(stepNames).hasSize(1).contains("Committing Entities");
    }

    @Test
    public void testFlatFileProjectCreationSteps() {
        List<String> stepNames = JobSteps.getJobSteps(JobType.FLAT_FILE_PROJECT_CREATION);
        assertThat(stepNames).hasSize(5);
        assertThat(stepNames.get(0)).isEqualTo("Uploading Flat Files");
        assertThat(stepNames.get(1)).isEqualTo("Parsing Artifact Files");
        assertThat(stepNames.get(2)).isEqualTo("Parsing Trace Files");
        assertThat(stepNames.get(3)).isEqualTo("Generating Trace Links");
        assertThat(stepNames.get(4)).isEqualTo("Committing Entities");
    }

    @Test
    public void testJiraProjectCreationSteps() {
        List<String> stepNames = JobSteps.getJobSteps(JobType.JIRA_PROJECT_CREATION);
        assertThat(stepNames).hasSize(5);
        assertThat(stepNames.get(0)).isEqualTo("Authenticating User Credentials");
        assertThat(stepNames.get(1)).isEqualTo("Retrieving Jira Project");
        assertThat(stepNames.get(2)).isEqualTo("Creating SAFA Project");
        assertThat(stepNames.get(3)).isEqualTo("Importing Issues and Links");
        assertThat(stepNames.get(4)).isEqualTo("Committing Entities");
    }

    @Test
    public void testJiraProjectUpdateSteps() {
        List<String> stepNames = JobSteps.getJobSteps(JobType.JIRA_PROJECT_UPDATE);
        assertThat(stepNames).hasSize(5);
        assertThat(stepNames.get(0)).isEqualTo("Authenticating User Credentials");
        assertThat(stepNames.get(1)).isEqualTo("Retrieving Jira Project");
        assertThat(stepNames.get(2)).isEqualTo("Creating SAFA Project");
        assertThat(stepNames.get(3)).isEqualTo("Importing Issues and Links");
        assertThat(stepNames.get(4)).isEqualTo("Committing Entities");
    }
}
