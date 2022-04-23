package unit.flatfile;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;

import java.util.HashMap;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.CommitError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.server.entities.db.TraceType;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.request.MockMultipartHttpServletRequestBuilder;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import unit.ApplicationBaseTest;
import unit.SampleProjectConstants;

public class TestCreateProjectViaFlatFiles extends ApplicationBaseTest {

    @Test
    public void testUseCase() throws Exception {

        // Step 1 - Upload flat files
        String routeName = AppRoutes.Projects.FlatFiles.projectFlatFiles;
        MockMultipartHttpServletRequestBuilder request = createMultiPartRequest(routeName,
            ProjectPaths.PATH_TO_BEFORE_FILES);
        JSONObject responseBody = sendRequest(request, MockMvcResultMatchers.status().isCreated(), this.token);

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
            .isEqualTo(SampleProjectConstants.N_ARTIFACTS);

        // VP - Traces present in response
        JSONArray traces = projectJson.getJSONArray("traces");
        assertThat(traces.length())
            .as("all traces confirmed")
            .isGreaterThanOrEqualTo(SampleProjectConstants.N_LINKS);

        int nManual = (int) traces
            .toList()
            .stream()
            .filter((traceJson) ->
                ((HashMap) traceJson).get("traceType").equals(TraceType.MANUAL.toString())
            ).count();
        assertThat(nManual)
            .as("manual traced confirmed")
            .isEqualTo(SampleProjectConstants.N_LINKS);

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
        assertThat(traceError.get("activity")).isNotNull();

        // VP - Project warnings present in response
        JSONObject projectWarnings = responseBody.getJSONObject("warnings");
        assertThat(projectWarnings.keySet().size()).isGreaterThanOrEqualTo(1);

        // VP 3 - Resources were created
        List<ProjectVersion> projectVersions = projectVersionRepository.findByProject(project);
        assertThat(projectVersions.size()).as("# versions").isEqualTo(1);
        ProjectVersion projectVersion = projectVersions.get(0);
        assertThat(projectVersion).as("project version created").isNotNull();

        // VP - Project types
        List<ArtifactType> projectTypes = artifactTypeRepository.findByProject(project);
        assertThat(projectTypes.size()).as("all types created").isEqualTo(SampleProjectConstants.N_TYPES);

        // VP - requirements created
        Optional<ArtifactType> requirementType = artifactTypeRepository
            .findByProjectAndNameIgnoreCase(project, "requirement");
        assertThat(requirementType.isPresent()).as("requirement type created").isTrue();
        List<Artifact> requirements = artifactRepository.findByProjectAndType(project, requirementType.get());
        assertThat(requirements.size()).as("requirements created").isEqualTo(SampleProjectConstants.N_REQUIREMENTS);

        // VP - design definitions created
        Optional<ArtifactType> designType = artifactTypeRepository
            .findByProjectAndNameIgnoreCase(project, "design");
        assertThat(designType.isPresent()).as("design type created").isTrue();
        List<Artifact> designs = artifactRepository.findByProjectAndType(project, designType.get());
        assertThat(designs.size())
            .as("designs created)")
            .isEqualTo(SampleProjectConstants.N_DESIGNS);

        // VP - hazards created
        Optional<ArtifactType> hazardType = artifactTypeRepository
            .findByProjectAndNameIgnoreCase(project, "HAZARD");
        assertThat(hazardType.isPresent()).as("hazard type created").isTrue();
        List<Artifact> hazards = artifactRepository.findByProjectAndType(project, hazardType.get());
        assertThat(hazards.size())
            .as("hazards created")
            .isEqualTo(SampleProjectConstants.N_HAZARDS);

        // VP - environment assumption artifacts created
        Optional<ArtifactType> envAssumptionType = artifactTypeRepository.findByProjectAndNameIgnoreCase(project,
            "EnvironmentalAssumption");
        assertThat(envAssumptionType.isPresent()).as("environment assumption type created")
            .isTrue();
        List<Artifact> envAssumptions = artifactRepository.findByProjectAndType(project, envAssumptionType.get());
        assertThat(envAssumptions.size())
            .as("env assumptions created")
            .isEqualTo(SampleProjectConstants.N_ENV_ASSUMPTIONS);

        List<Artifact> projectArtifacts = artifactRepository.getProjectArtifacts(project);
        assertThat(projectArtifacts.size()).isEqualTo(SampleProjectConstants.N_ARTIFACTS);

        // VP - Artifact bodies
        List<ArtifactVersion> artifactBodies = artifactVersionRepository.findByProjectVersion(projectVersion);
        assertThat(artifactBodies.size())
            .as("artifact bodies created")
            .isEqualTo(SampleProjectConstants.N_ARTIFACTS);

        List<CommitError> commitErrors = commitErrorRepository.findByProjectVersion(projectVersion);
        assertThat(commitErrors.size()).as("requirement parsing errors").isEqualTo(1);
        CommitError error = commitErrors.get(0);
        assertThat(error.getApplicationActivity()).isEqualTo(ProjectEntity.TRACES);

        List<TraceLinkVersion> traceLinks = traceLinkVersionRepository.getApprovedLinksInVersion(projectVersion);
        assertThat(traceLinks.size()).isEqualTo(SampleProjectConstants.N_LINKS);

        projectService.deleteProject(project);
    }

    /**
     * Creates three project versions and uploads to the middle one checking that
     * the first has no entities while the last has all the entities but no changes.
     *
     * @throws Exception If https request fails.
     */
    @Test
    public void testUpdateProjectViaFlatFiles() throws Exception {
        String projectName = "test-project";

        // Step - Create project with three versions
        dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newVersion(projectName)
            .newVersion(projectName);
        Project project = dbEntityBuilder.getProject(projectName);
        ProjectVersion emptyVersion = dbEntityBuilder.getProjectVersion(projectName, 0);
        ProjectVersion updateVersion = dbEntityBuilder.getProjectVersion(projectName, 1);
        ProjectVersion noChangeVersion = dbEntityBuilder.getProjectVersion(projectName, 2);

        // Step - Create request to update project via flat files
        uploadFlatFilesToVersion(updateVersion, ProjectPaths.PATH_TO_BEFORE_FILES);

        // VP - Verify that no artifacts associated with empty version
        List<ArtifactVersion> initialBodies = this.artifactVersionRepository.findByProjectVersion(emptyVersion);
        assertThat(initialBodies.size())
            .as("no bodies at init")
            .isEqualTo(0);

        // VP - Verify that artifacts are constructed and associated with update version
        List<ArtifactVersion> updateBodies = this.artifactVersionRepository.findByProjectVersion(updateVersion);
        assertThat(updateBodies.size())
            .as("bodies created in later version")
            .isEqualTo(SampleProjectConstants.N_ARTIFACTS);
        List<TraceLinkVersion> updateTraces = this.traceLinkVersionRepository.getApprovedLinksInProject(project);
        assertThat(updateTraces.size()).isEqualTo(SampleProjectConstants.N_LINKS);

        // Step - Create request to parse same flat files at different version
        uploadFlatFilesToVersion(noChangeVersion, ProjectPaths.PATH_TO_BEFORE_FILES);

        // VP - No new artifacts were created
        List<ArtifactVersion> noChangeBodies = this.artifactVersionRepository.findByProjectVersion(noChangeVersion);
        assertThat(noChangeBodies.size())
            .as("no changes were detected in project versions")
            .isEqualTo(0);

        // VP - No new trace links were created
        List<TraceLinkVersion> noChangeTraces = this.traceLinkVersionRepository.getApprovedLinksInProject(project);
        assertThat(noChangeTraces.size()).isEqualTo(SampleProjectConstants.N_LINKS);
    }
}
