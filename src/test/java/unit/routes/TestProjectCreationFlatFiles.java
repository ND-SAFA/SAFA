package unit.routes;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.db.entities.sql.ApplicationActivity;
import edu.nd.crc.safa.db.entities.sql.Artifact;
import edu.nd.crc.safa.db.entities.sql.ArtifactBody;
import edu.nd.crc.safa.db.entities.sql.ArtifactType;
import edu.nd.crc.safa.db.entities.sql.ParserError;
import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.db.entities.sql.TraceLink;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.request.MockMultipartHttpServletRequestBuilder;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import unit.EntityBaseTest;
import unit.MultipartHelper;
import unit.TestConstants;
import unit.TestUtil;

public class TestProjectCreationFlatFiles extends EntityBaseTest {

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

        // VP 1 - Server response is 200 - okay
        assertThat(response).as("server response non-null").isNotNull();
        JSONObject responseContent = TestUtil.asJson(response);
        assertThat(responseContent.get("status")).as("status is set").isEqualTo(0);
        JSONObject responseBody = responseContent.getJSONObject("body");
        assertThat(responseBody).as("response body is non-null").isNotNull();

        // VP 2 - API Response object
        JSONObject projectJson = responseBody.getJSONObject("project");
        assertThat(projectJson).as("uploadedFiles non-null").isNotNull();
        String projectId = projectJson.getString("projectId");
        Project project = projectRepository.findByProjectId(UUID.fromString(projectId));
        assertThat(project).as("project was created").isNotNull();
        assertThat(projectJson.getJSONArray("artifacts").length())
            .as("all artifacts confirmed")
            .isEqualTo(TestConstants.N_ARTIFACTS);
        assertThat(projectJson.getJSONArray("traces").length())
            .as("all traces confirmed")
            .isEqualTo(TestConstants.N_LINKS);
        JSONObject errors = responseBody.getJSONObject("errors");
        assertThat(errors.getJSONArray("tim").length())
            .as("tim file error")
            .isEqualTo(0);
        assertThat(errors.getJSONArray("artifacts").length())
            .as("artifact parsing errors")
            .isEqualTo(0);
        assertThat(errors.getJSONArray("traces").length())
            .as("trace link errors")
            .isEqualTo(1);

        JSONObject traceError = errors.getJSONArray("traces").getJSONObject(0);
        assertThat(traceError.get("errorId")).isNotNull();
        assertThat(traceError.get("message")).isNotNull();
        assertThat(traceError.get("location")).isNotNull();
        assertThat(traceError.get("activity")).isNotNull();

        // VP 3 - Resources were created
        List<ProjectVersion> projectVersions = projectVersionRepository.findByProject(project);
        assertThat(projectVersions.size()).as("# versions").isEqualTo(1);
        ProjectVersion projectVersion = projectVersions.get(0);
        assertThat(projectVersion).as("project version created").isNotNull();

        // VP - Project types
        List<ArtifactType> projectTypes = artifactTypeRepository.findByProject(project);
        assertThat(projectTypes.size()).as("all types created").isEqualTo(TestConstants.N_TYPES);

        // VP - requirements created
        Optional<ArtifactType> requirementType = artifactTypeRepository
            .findByProjectAndNameIgnoreCase(project, "requirement");
        assertThat(requirementType.isPresent()).as("requirement type created").isTrue();
        List<Artifact> requirements = artifactRepository.findByProjectAndType(project, requirementType.get());
        assertThat(requirements.size()).as("requirements created").isEqualTo(TestConstants.N_REQUIREMENTS);

        // VP - design definitions created
        Optional<ArtifactType> designType = artifactTypeRepository
            .findByProjectAndNameIgnoreCase(project, "design");
        assertThat(designType.isPresent()).as("design type created").isTrue();
        List<Artifact> designs = artifactRepository.findByProjectAndType(project, designType.get());
        assertThat(designs.size())
            .as("designs created)")
            .isEqualTo(TestConstants.N_DESIGNS);

        // VP - hazards created
        Optional<ArtifactType> hazardType = artifactTypeRepository
            .findByProjectAndNameIgnoreCase(project, "HAZARD");
        assertThat(hazardType.isPresent()).as("hazard type created").isTrue();
        List<Artifact> hazards = artifactRepository.findByProjectAndType(project, hazardType.get());
        assertThat(hazards.size())
            .as("hazards created")
            .isEqualTo(TestConstants.N_HAZARDS);

        // VP - environment assumption artifacts created
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

        // VP - Artifact bodies
        List<ArtifactBody> artifactBodies = artifactBodyRepository.findByProjectVersion(projectVersion);
        assertThat(artifactBodies.size())
            .as("artifact bodies created")
            .isEqualTo(TestConstants.N_ARTIFACTS);

        List<ParserError> parserErrors = parserErrorRepository.findByProjectVersion(projectVersion);
        assertThat(parserErrors.size()).as("requirement parsing errors").isEqualTo(1);
        ParserError error = parserErrors.get(0);
        assertThat(error.getApplicationActivity()).isEqualTo(ApplicationActivity.PARSING_TRACES);
        assertThat(error.getFileName()).isEqualTo("Requirement2Requirement.csv");

        List<TraceLink> traceLinks = traceLinkRepository.findByProject(project);
        assertThat(traceLinks.size()).isEqualTo(TestConstants.N_LINKS);

        projectService.deleteProject(project);
    }
}
