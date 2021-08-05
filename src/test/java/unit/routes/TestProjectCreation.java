package unit.routes;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.constants.ProjectPaths;
import edu.nd.crc.safa.entities.Artifact;
import edu.nd.crc.safa.entities.ArtifactBody;
import edu.nd.crc.safa.entities.ArtifactType;
import edu.nd.crc.safa.entities.Project;
import edu.nd.crc.safa.entities.ProjectVersion;
import edu.nd.crc.safa.entities.TraceLink;
import edu.nd.crc.safa.services.ProjectService;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.request.MockMultipartHttpServletRequestBuilder;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import unit.EntityBaseTest;
import unit.MultipartHelper;
import unit.TestConstants;
import unit.TestUtil;

public class TestProjectCreation extends EntityBaseTest {

    @Autowired
    ProjectService projectService;

    @Test
    public void testMultipleFilesUploadRestController() throws Exception {

        String attributeName = "files";
        String routeName = "/projects/flat-files";

        List<MockMultipartFile> files =
            MultipartHelper.createMockMultipartFilesFromDirectory(ProjectPaths.PATH_TO_TEST_RESOURCES,
                attributeName);
        MockMultipartHttpServletRequestBuilder request = multipart(routeName);

        for (MockMultipartFile file : files) {
            request.file(file);
        }

        MvcResult response = mockMvc
            .perform(request)
            .andExpect(MockMvcResultMatchers.status().isCreated())
            .andReturn();

        //Verification Points
        // VP 1 - Server response is non-null and has contains status
        assertThat(response).as("server response non-null").isNotNull();
        JSONObject responseContent = TestUtil.asJson(response);
        assertThat(responseContent.get("status")).as("status is set").isEqualTo(0);
        JSONObject responseBody = responseContent.getJSONObject("body");
        assertThat(responseBody).as("response body is non-null").isNotNull();

        // VP 2 - Files were successfully uploaded to server.
        JSONObject flatFileResponse = responseBody.getJSONObject("flatFileResponse");
        assertThat(flatFileResponse).as("flat file response non-null").isNotNull();

        JSONArray filesReceived = flatFileResponse.getJSONArray("uploadedFiles");
        assertThat(filesReceived).as("uploadedFiles non-null").isNotNull();
        assertThat(filesReceived.length()).as("all files uploaded").isEqualTo(3);

        // VP 3 - Resources were created
        JSONObject projectJson = responseBody.getJSONObject("project");
        String projectId = projectJson.getString("projectId");
        Project project = projectRepository.findByProjectId(UUID.fromString(projectId));
        assertThat(project).as("project was created").isNotNull();

        ProjectVersion projectVersion = projectVersionRepository.findTopByProjectOrderByVersionIdDesc(project);
        assertThat(projectVersion).as("project version created").isNotNull();

        List<ArtifactType> projectTypes = artifactTypeRepository.findByProject(project);
        assertThat(projectTypes.size()).as("all types created").isEqualTo(TestConstants.N_TYPES);

        List<Artifact> projectArtifacts = artifactRepository.findByProject(project);
        assertThat(projectArtifacts.size()).isEqualTo(TestConstants.N_DESIGN_ARTIFACTS);

        List<ArtifactBody> artifactBodies = artifactBodyRepository.findByProjectVersion(projectVersion);
        assertThat(artifactBodies.size())
            .as("artifact bodies created")
            .isEqualTo(TestConstants.N_DESIGN_ARTIFACTS);

        List<TraceLink> traceLinks = traceLinkRepository.findByProject(project);
        assertThat(traceLinks.size()).isEqualTo(TestConstants.N_LINKS);

        projectService.deleteProject(project);
    }
}
