package unit.controllers.project;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;

import java.util.HashMap;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.db.entities.sql.ApplicationActivity;
import edu.nd.crc.safa.server.db.entities.sql.Artifact;
import edu.nd.crc.safa.server.db.entities.sql.ArtifactBody;
import edu.nd.crc.safa.server.db.entities.sql.ArtifactType;
import edu.nd.crc.safa.server.db.entities.sql.ParserError;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.db.entities.sql.TraceApproval;
import edu.nd.crc.safa.server.db.entities.sql.TraceLink;
import edu.nd.crc.safa.server.db.entities.sql.TraceType;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.request.MockMultipartHttpServletRequestBuilder;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import unit.EntityBaseTest;
import unit.TestConstants;

public class TestProjectCreationFlatFiles extends EntityBaseTest {

    @Test
    public void testMultipleFilesUploadRestController() throws Exception {

        String routeName = "/projects/flat-files";

        MockMultipartHttpServletRequestBuilder request = createMultiPartRequest(routeName,
            ProjectPaths.PATH_TO_BEFORE_FILES);
        JSONObject responseContent = sendRequest(request, MockMvcResultMatchers.status().isCreated());

        // VP 1 - Server response is 200 - okay
        assertThat(responseContent.get("status")).as("status is set").isEqualTo(0);
        JSONObject responseBody = responseContent.getJSONObject("body");
        assertThat(responseBody).as("response body is non-null").isNotNull();

        // Step - Get JSON Response
        JSONObject projectJson = responseBody.getJSONObject("project");

        // VP - Project id is not null
        assertThat(projectJson).as("uploadedFiles non-null").isNotNull();
        String projectId = projectJson.getString("projectId");

        // VP - Project with id was created
        Project project = projectRepository.findByProjectId(UUID.fromString(projectId));
        assertThat(project).as("project was created").isNotNull();

        // VP - Artifacts present in response
        assertThat(projectJson.getJSONArray("artifacts").length())
            .as("all artifacts confirmed")
            .isEqualTo(TestConstants.N_ARTIFACTS);

        // VP - Traces present in response
        assertThat(projectJson.getJSONArray("traces").length())
            .as("all traces confirmed")
            .isGreaterThanOrEqualTo(TestConstants.N_LINKS);
        int nManual = (int) projectJson.getJSONArray("traces")
            .toList()
            .stream()
            .filter((traceJson) ->
                ((HashMap) traceJson).get("traceType").equals(TraceType.MANUAL.toString())
            ).count();
        assertThat(nManual)
            .as("manual traced confirmed")
            .isEqualTo(TestConstants.N_LINKS);

        // VP - Errors are present in response
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

        // VP - Project warnings present in response
        JSONObject projectWarnings = responseBody.getJSONObject("warnings");
        assertThat(projectWarnings.keySet().size()).isGreaterThanOrEqualTo(2);

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

        List<TraceLink> traceLinks = traceLinkRepository
            .findBySourceArtifactProjectAndApprovalStatus(project, TraceApproval.APPROVED);
        assertThat(traceLinks.size()).isEqualTo(TestConstants.N_LINKS);

        projectService.deleteProject(project);
    }

    @Test
    public void testUpdateProjectViaFlatFiles() throws Exception {
        String projectName = "test-project";

        entityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newVersion(projectName)
            .newVersion(projectName);

        Project project = entityBuilder.getProject(projectName);
        ProjectVersion emptyVersion = entityBuilder.getProjectVersion(projectName, 0);
        ProjectVersion updateVersion = entityBuilder.getProjectVersion(projectName, 1);
        ProjectVersion noChangeVersion = entityBuilder.getProjectVersion(projectName, 2);

        // Step - Create request to update project via flat files
        String updateRouteName = String.format("/projects/%s/%s/flat-files",
            project.getProjectId().toString(),
            updateVersion.getVersionId().toString());

        MockMultipartHttpServletRequestBuilder updateRequest = createMultiPartRequest(updateRouteName,
            ProjectPaths.PATH_TO_BEFORE_FILES);
        sendRequest(updateRequest, MockMvcResultMatchers.status().isCreated());

        // VP - Verify that no artifacts associated with empty version
        List<ArtifactBody> initialBodies = this.artifactBodyRepository.findByProjectVersion(emptyVersion);
        assertThat(initialBodies.size())
            .as("no bodies at init")
            .isEqualTo(0);

        // VP - Verify that artifacts are constructed and associated with update version
        List<ArtifactBody> updateBodies = this.artifactBodyRepository.findByProjectVersion(updateVersion);
        assertThat(updateBodies.size())
            .as("bodies created in later version")
            .isEqualTo(TestConstants.N_ARTIFACTS);
        List<TraceLink> updateTraces = this.traceLinkRepository.getApprovedLinks(project);
        assertThat(updateTraces.size()).isEqualTo(TestConstants.N_LINKS);

        // Step - Create request to parse same flat files at different version
        String noChangeRouteName = String.format("/projects/%s/%s/flat-files",
            project.getProjectId().toString(),
            noChangeVersion.getVersionId().toString());
        MockMultipartHttpServletRequestBuilder noChangeRequest = createMultiPartRequest(noChangeRouteName,
            ProjectPaths.PATH_TO_BEFORE_FILES);
        sendRequest(noChangeRequest, MockMvcResultMatchers.status().isCreated());

        // VP - No new artifacts were created
        List<ArtifactBody> noChangeBodies = this.artifactBodyRepository.findByProjectVersion(noChangeVersion);
        assertThat(noChangeBodies.size())
            .as("no changes were detected in project versions")
            .isEqualTo(0);

        // VP - No new trace links were created
        List<TraceLink> noChangeTraces = this.traceLinkRepository.getApprovedLinks(project);
        assertThat(noChangeTraces.size()).isEqualTo(TestConstants.N_LINKS);
    }
}
