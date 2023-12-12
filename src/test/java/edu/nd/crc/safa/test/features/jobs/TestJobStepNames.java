package edu.nd.crc.safa.test.features.jobs;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;

import edu.nd.crc.safa.features.jobs.JobExecutionUtilities;
import edu.nd.crc.safa.features.jobs.entities.app.JobSteps;
import edu.nd.crc.safa.features.jobs.entities.jobs.CreateProjectViaJiraJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.CreateProjectViaJsonJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.FlatFileProjectCreationJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.HGenJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.JiraProjectUpdateJob;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;

import org.junit.jupiter.api.Test;

/**
 * Tests that the correct steps are retrieved for each available job.
 */
class TestJobStepNames extends ApplicationBaseTest {
    @Test
    void negativeIndices() {
        assertThat(JobExecutionUtilities.getStepIndex(-1, 1)).isEqualTo(0);
        assertThat(JobExecutionUtilities.getStepIndex(-2, 5)).isEqualTo(3);
    }

    @Test
    void testCommitJobSteps() {
        List<String> stepNames = JobSteps.getJobSteps(CreateProjectViaJsonJob.class);
        String[] expectedStepNames = new String[]{
            "Creating Project",
            "Generating Trace Links",
            "Committing Entities",
            "Done"
        };
        testStepNames(expectedStepNames, stepNames);
    }

    @Test
    void testFlatFileProjectCreationSteps() {
        List<String> stepNames = JobSteps.getJobSteps(FlatFileProjectCreationJob.class);
        String[] expectedStepNames = new String[]{
            "Parsing Files",
            "Summarizing Code Artifacts",
            "Generating Trace Links",
            "Committing Entities",
            "Done"
        };
        testStepNames(expectedStepNames, stepNames);
    }

    @Test
    void testHGenSteps() {
        List<String> stepNames = JobSteps.getJobSteps(HGenJob.class);
        String[] expectedStepNames = new String[]{
            "Retrieving Project",
            "Summarizing Project Entities",
            "Generating Artifacts",
            "Committing Entities",
            "Done"
        };
        testStepNames(expectedStepNames, stepNames);
    }

    @Test
    void testJiraProjectCreationSteps() {
        List<String> stepNames = JobSteps.getJobSteps(CreateProjectViaJiraJob.class);
        String[] expectedStepNames = getJiraStepNames();
        testStepNames(expectedStepNames, stepNames);
    }

    @Test
    void testJiraProjectUpdateSteps() {
        List<String> stepNames = JobSteps.getJobSteps(JiraProjectUpdateJob.class);
        String[] expectedStepNames = getJiraStepNames();
        testStepNames(expectedStepNames, stepNames);
    }


    private String[] getJiraStepNames() {
        return new String[]{
            "Authenticating User Credentials",
            "Retrieving Jira Project",
            "Creating SAFA Project",
            "Creating SAFA Project to Jira Project Mapping",
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
