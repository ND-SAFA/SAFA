package unit.project.json;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceLinkVersion;

import org.json.JSONObject;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;

/**
 * Tests that user is able to submit a project creation job via JSON.
 */
class TestJSONBaseJobUpload extends ProjectJsonBaseTest {

    /**
     * Test that user is able to update project with checks for:
     * TODO: Update this test to use the job module in a subsequent PR
     */
    @Test
    @Disabled("Not implemented yet")
    void updateEntities() throws Exception {
        // Step - Create Project JSON
        JSONObject projectJson = createBaseProjectJson();

        // Step - Create project via JSON
        JSONObject responseContent = postProjectJson(projectJson);
        String projectId = responseContent
            .getString("projectId");
        String versionId = responseContent
            .getJSONObject("projectVersion")
            .getString("versionId");
        Project project = this.projectRepository.findByProjectId(UUID.fromString(projectId));
        List<ArtifactVersion> artifactBodiesQuery =
            this.artifactVersionRepository.getBodiesWithName(project, a1Name);
        assertThat(artifactBodiesQuery.size()).as("# of bodies on init").isEqualTo(1);

        // Step - Create Updated Request and Send
        String newProjectName = "new-project-name";
        JSONObject updateRequestJson = jsonBuilder
            .withProject(projectId, newProjectName, projectDescription)
            .withProjectVersion(newProjectName, versionId, 1, 1, 2)
            .getProjectJson(newProjectName);
        postProjectJson(updateRequestJson);

        // VP - Verify that project name has changed
        verifyProjectInformation(UUID.fromString(projectId), newProjectName, projectDescription);
    }


    private void testProjectArtifactsCreated(Project project, int expectedVersions) {
        // VP - Resources were created
        List<ProjectVersion> projectVersions = projectVersionRepository.findByProject(project);
        assertThat(projectVersions.size()).as("# versions").isEqualTo(expectedVersions);
        ProjectVersion projectVersion = projectVersions.get(0);
        assertThat(projectVersion).as("project version created").isNotNull();

        // VP - Project types are created
        List<ArtifactType> projectTypes = artifactTypeRepository.findByProject(project);
        assertThat(projectTypes.size()).as("all types created").isEqualTo(N_TYPES);

        // VP - requirements created
        Optional<ArtifactType> requirementType = artifactTypeRepository
            .findByProjectAndNameIgnoreCase(project, "requirement");
        assertThat(requirementType).as("requirement type created").isPresent();
        List<Artifact> requirements = artifactRepository.findByProjectAndType(project, requirementType.get());
        assertThat(requirements).as("requirements created").hasSize(1);

        // VP - design definitions created
        Optional<ArtifactType> designType = artifactTypeRepository
            .findByProjectAndNameIgnoreCase(project, "design");
        assertThat(designType).as("design type created").isPresent();
        List<Artifact> designs = artifactRepository.findByProjectAndType(project, designType.get());
        assertThat(designs.size())
            .as("designs created)")
            .isEqualTo(1);

        List<Artifact> projectArtifacts = artifactRepository.getProjectArtifacts(project);
        assertThat(projectArtifacts.size()).isEqualTo(N_ARTIFACTS);

        // VP - Artifact bodies
        List<ArtifactVersion> artifactBodies = artifactVersionRepository.findByProjectVersion(projectVersion);
        assertThat(artifactBodies.size())
            .as("artifact bodies created")
            .isEqualTo(N_ARTIFACTS);
        List<TraceLinkVersion> traceLinks = traceLinkVersionRepository.getApprovedLinksInVersion(projectVersion);
        assertThat(traceLinks.size()).isEqualTo(N_TRACES);
    }
}
