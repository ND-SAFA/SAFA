package edu.nd.crc.safa.test.features.generation;

import static org.junit.jupiter.api.Assertions.assertEquals;

import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.services.CommonRequestService;

import org.junit.jupiter.api.Test;

class TestProjectSummary extends GenerationalTest {
    /**
     * Tests that project summary job sets the project description.
     */
    @Test
    void testProjectDescriptionIsSet() throws Exception {
        createProject();
        mockProjectSummaryResponse();
        runProjectSummaryJob();

        refreshProject();

        String projectSummary = getProject().getDescription();
        String specification = getProject().getSpecification();

        assertEquals(getProjectSummary(), projectSummary);
        assertEquals(getProjectSummary(), specification);
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

        assertEquals(getProjectSummary(), getProject().getDescription());
        assertEquals(newSummary, getProject().getSpecification());
    }

    private void runProjectSummaryJob() throws Exception {
        ProjectVersion projectVersion = getProjectVersion();
        CommonRequestService.Gen.performProjectSummary(projectVersion);
    }
}
