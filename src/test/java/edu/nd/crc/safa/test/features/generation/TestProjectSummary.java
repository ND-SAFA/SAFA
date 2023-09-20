package edu.nd.crc.safa.test.features.generation;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.ArrayList;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.generation.projectsummary.ProjectSummaryResponse;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;

class TestProjectSummary extends AbstractGenerationTest {
    private final String summary = "project-summary";

    /**
     * Tests that project summary job sets the project description.
     */
    @Test
    void testProjectDescriptionIsSet() throws Exception {
        ProjectVersion projectVersion = creationService.createProjectWithNewVersion(projectName);
        setProjectSummaryResponse(summary);

        JSONObject project = runProjectSummaryJob(projectVersion);

        String projectSummary = project.getString("description");
        String specification = project.getString("specification");

        assertEquals(projectSummary, summary);
        assertEquals(specification, summary);
    }

    /**
     * Tests that project summary can be updated.
     */
    @Test
    void testProjectSummaryUpdate() throws Exception {
        ProjectVersion projectVersion = creationService.createProjectWithNewVersion(projectName);
        String newSummary = "new-summary";

        setProjectSummaryResponse(summary);
        runProjectSummaryJob(projectVersion);

        mockServer.reset();

        setProjectSummaryResponse(newSummary);
        JSONObject project = runProjectSummaryJob(projectVersion);

        assertEquals(summary, project.getString("description"));
        assertEquals(newSummary, project.getString("specification"));
    }

    private JSONObject runProjectSummaryJob(ProjectVersion projectVersion) throws Exception {
        JSONObject payload = new JSONObject();

        SafaRequest
            .withRoute(AppRoutes.Summarize.SUMMARIZE_PROJECT)
            .withVersion(projectVersion)
            .postWithJsonObject(payload, JobAppEntity.class);

        JSONObject project = SafaRequest
            .withRoute(AppRoutes.Retrieval.GET_PROJECT_IN_VERSION)
            .withVersion(projectVersion)
            .getWithJsonObject();
        return project;
    }

    private void setProjectSummaryResponse(String summary) {
        ProjectSummaryResponse mockResponse = new ProjectSummaryResponse();
        mockResponse.setSummary(summary);
        mockResponse.setArtifacts(new ArrayList<>());
        setProjectSummaryResponse(mockResponse);
    }
}
