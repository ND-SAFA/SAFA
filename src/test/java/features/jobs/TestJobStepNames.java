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
class TestJobStepNames extends ApplicationBaseTest {
    @Test
    void negativeIndices() {
        assertThat(AbstractJob.getStepIndex(-1, 1)).isEqualTo(0);
        assertThat(AbstractJob.getStepIndex(-2, 5)).isEqualTo(3);
    }

    @Test
    void testCommitJobSteps() {
        List<String> stepNames = JobSteps.getJobSteps(JobType.PROJECT_CREATION_VIA_JSON);
        String[] expectedStepNames = new String[]{
            "Generating Trace Links",
            "Committing Entities",
            "Done"
        };
        testStepNames(expectedStepNames, stepNames);
    }

    @Test
    void testFlatFileProjectCreationSteps() {
        List<String> stepNames = JobSteps.getJobSteps(JobType.PROJECT_CREATION_VIA_FLAT_FILE);
        String[] expectedStepNames = new String[]{
            "Uploading Flat Files",
            "Parsing Files",
            "Generating Trace Links",
            "Committing Entities",
            "Done"
        };
        testStepNames(expectedStepNames, stepNames);
    }

    @Test
    void testJiraProjectCreationSteps() {
        List<String> stepNames = JobSteps.getJobSteps(JobType.PROJECT_CREATION_VIA_JIRA);
        String[] expectedStepNames = getJiraStepNames();
        testStepNames(expectedStepNames, stepNames);
    }

    @Test
    void testJiraProjectUpdateSteps() {
        List<String> stepNames = JobSteps.getJobSteps(JobType.PROJECT_UPDATE_VIA_JIRA);
        String[] expectedStepNames = getJiraStepNames();
        testStepNames(expectedStepNames, stepNames);
    }

    private String[] getJiraStepNames() {
        return new String[]{
            "Authenticating User Credentials",
            "Retrieving Jira Project",
            "Creating SAFA Project",
            "Importing Issues and Links",
            "Committing Entities",
            "Done"
        };
    }

    private void testStepNames(String[] expectedNames, List<String> stepNames) {
        assertThat(stepNames).hasSize(expectedNames.length);
        for (int i = 0; i < expectedNames.length; i++) {
            String expectedStepName = expectedNames[i];
            String stepName = stepNames.get(i);
            assertThat(stepName).isEqualToIgnoringCase(expectedStepName);
        }
    }
}
