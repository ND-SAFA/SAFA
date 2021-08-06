package unit.routes;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.constants.ProjectPaths;
import edu.nd.crc.safa.entities.ApplicationActivity;
import edu.nd.crc.safa.entities.Artifact;
import edu.nd.crc.safa.entities.ArtifactBody;
import edu.nd.crc.safa.entities.ArtifactType;
import edu.nd.crc.safa.entities.ParserError;
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
        assertThat(filesReceived.length()).as("all files uploaded").isEqualTo(TestConstants.N_FILES);

        // VP 3 - Resources were created
        JSONObject projectJson = responseBody.getJSONObject("project");
        String projectId = projectJson.getString("projectId");
        Project project = projectRepository.findByProjectId(UUID.fromString(projectId));
        assertThat(project).as("project was created").isNotNull();

        List<ProjectVersion> projectVersions = projectVersionRepository.findByProject(project);
        assertThat(projectVersions.size()).as("# versions").isEqualTo(1);
        ProjectVersion projectVersion = projectVersions.get(0);
        assertThat(projectVersion).as("project version created").isNotNull();

        // VP X - Project types
        List<ArtifactType> projectTypes = artifactTypeRepository.findByProject(project);
        assertThat(projectTypes.size()).as("all types created").isEqualTo(TestConstants.N_TYPES);

        // VP X - requirements artifacts created
        Optional<ArtifactType> requirementType = artifactTypeRepository
            .findByProjectAndNameIgnoreCase(project, "requirement");
        assertThat(requirementType.isPresent()).as("requirement type created").isTrue();
        List<Artifact> requirements = artifactRepository.findByProjectAndType(project, requirementType.get());
        assertThat(requirements.size()).as("requirements created").isEqualTo(TestConstants.N_REQUIREMENTS);

        // VP X - design artifacts created
        Optional<ArtifactType> designType = artifactTypeRepository
            .findByProjectAndNameIgnoreCase(project, "design");
        assertThat(designType.isPresent()).as("design type created").isTrue();
        List<Artifact> designs = artifactRepository.findByProjectAndType(project, designType.get());
        assertThat(designs.size())
            .as("designs created)")
            .isEqualTo(TestConstants.N_DESIGNS);

        // VP X - hazards artifacts created
        Optional<ArtifactType> hazardType = artifactTypeRepository
            .findByProjectAndNameIgnoreCase(project, "hazard");
        assertThat(hazardType.isPresent()).as("hazard type created").isTrue();
        List<Artifact> hazards = artifactRepository.findByProjectAndType(project, hazardType.get());
        assertThat(hazards.size())
            .as("hazards created")
            .isEqualTo(TestConstants.N_HAZARDS);

        // VP X - environment assumption artifacts created
        Optional<ArtifactType> envAssumptionType = artifactTypeRepository.findByProjectAndNameIgnoreCase(project,
            "EnvironmentalAssumption");
        assertThat(envAssumptionType.isPresent()).as("environment assumption type created")
            .isTrue();
        List<Artifact> envAssumptions = artifactRepository.findByProjectAndType(project, envAssumptionType.get());
        assertThat(envAssumptions.size())
            .as("env assumptions created")
            .isEqualTo(TestConstants.N_ENV_ASSUMPTIONS);

        List<Artifact> projectArtifacts = artifactRepository.findByProject(project);
        assertThat(projectArtifacts.size()).isEqualTo(TestConstants.N_ARTIFACTS);

        // VP X - Artifact bodies
        List<ArtifactBody> artifactBodies = artifactBodyRepository.findByProjectVersion(projectVersion);
        assertThat(artifactBodies.size())
            .as("artifact bodies created")
            .isEqualTo(TestConstants.N_ARTIFACTS);

        List<ParserError> parserErrors = parserErrorRepository.findByProject(project);
        assertThat(parserErrors.size()).as("requirement parsing errors").isEqualTo(1);
        ParserError error = parserErrors.get(0);
        assertThat(error.getActivity()).isEqualTo(ApplicationActivity.PARSING_TRACE_MATRIX);
        assertThat(error.getFileName()).isEqualTo("Requirement2Requirement.csv");

        List<TraceLink> traceLinks = traceLinkRepository.findByProject(project);
        assertThat(traceLinks.size()).isEqualTo(TestConstants.N_LINKS);

        projectService.deleteProject(project);
    }
}
