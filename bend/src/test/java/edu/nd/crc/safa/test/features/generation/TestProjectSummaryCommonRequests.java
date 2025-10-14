package edu.nd.crc.safa.test.features.generation;

import static org.junit.jupiter.api.Assertions.assertEquals;

import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.services.GenTestService;
import edu.nd.crc.safa.test.services.requests.GenCommonRequests;

import org.junit.jupiter.api.Test;

class TestProjectSummaryCommonRequests extends GenerationalTest {
    /**
     * Tests that project summary job sets the project description.
     */
    @Test
    void testProjectDescriptionIsSet() throws Exception {
        createProject();
        mockProjectSummaryResponse();

        JobAppEntity job = runProjectSummaryJob();

        refreshProject();

        String specification = getProject().getSpecification();

        assertEquals(getProjectSummary(), specification);
        GenTestService.verifyJobAssociatedWithProject(this, job);
    }

    /**
     * Tests that project summary can be updated.
     */
    @Test
    void testProjectSummaryUpdate() throws Exception {
        createProject();
        mockProjectSummaryResponse();
        runProjectSummaryJob();

        String newSummary = "new-summary";
        mockProjectSummaryResponse(newSummary);

        runProjectSummaryJob();

        refreshProject();

        assertEquals(newSummary, getProject().getSpecification());
    }

    private JobAppEntity runProjectSummaryJob() throws Exception {
        ProjectVersion projectVersion = getProjectVersion();
        return GenCommonRequests.performProjectSummary(projectVersion);
    }
}
