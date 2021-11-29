package unit.project.json;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactBody;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceLink;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Tests that user is able to create and update a project via JSON.
 */
public class TestProjectCreateOrProject extends BaseProjectJsonTest {

    @Autowired
    ObjectMapper objectMapper;

    /**
     * Tests that all entities in the given request created. Namely,
     * - a source artifact + requirement type
     * - a target artifact + design type
     * - a trace link (between artifacts)
     */
    @Test
    public void createEntitiesFromJson() throws Exception {
        JSONObject projectJson = createBaseProjectJson();
        JSONObject responseContent = postProjectJson(projectJson);
        String projectId = responseContent
            .getJSONObject("body")
            .getJSONObject("project")
            .getString("projectId");
        Project project = this.projectRepository.findByProjectId(UUID.fromString(projectId));
        testProjectArtifactsCreated(project, 1);
        projectService.deleteProject(project);
    }

    /**
     * Test that user is able to update project with checks for:
     */
    @Test
    public void updateEntities() throws Exception {
        // Step - Create Project containing:
        JSONObject projectJson = createBaseProjectJson();
        JSONObject responseContent = postProjectJson(projectJson);
        String projectId = responseContent
            .getJSONObject("body")
            .getJSONObject("project")
            .getString("projectId");
        String versionId = responseContent
            .getJSONObject("body")
            .getJSONObject("projectVersion")
            .getString("versionId");
        Project project = this.projectRepository.findByProjectId(UUID.fromString(projectId));
        testProjectArtifactsCreated(project, 1);
        List<ArtifactBody> artifactBodiesQuery =
            this.artifactBodyRepository.getBodiesWithName(project, a1Name);
        assertThat(artifactBodiesQuery.size()).as("# of bodies on init").isEqualTo(1);

        // Step - Create Updated Request and Send
        String newProjectName = "new-project-name";
        String newArtifactBody = "new-artifact-body";
        String artifactId = artifactBodiesQuery.get(0).getArtifact().getArtifactId().toString();
        JSONObject updateRequestJson = jsonBuilder
            .withProject(projectId, newProjectName, projectDescription)
            .withProjectVersion(newProjectName, versionId, 1, 1, 2)
            .withArtifact(newProjectName, artifactId, a1Name, a1Type, newArtifactBody)
            .getPayload(newProjectName);
        postProjectJson(updateRequestJson);

        // VP - Verify that project name has changed
        Project updatedProject = this.projectRepository.findByProjectId(UUID.fromString(projectId));
        assertThat(updatedProject.getName()).isEqualTo(newProjectName);
        // VP - Verify that entities still exist and no other version was created
        testProjectArtifactsCreated(project, 1);
        // VP - Verify that artifact has two versions and the latest has updated body.
        artifactBodiesQuery =
            this.artifactBodyRepository.getBodiesWithName(project, a1Name);
        assertThat(artifactBodiesQuery.size()).as("# of bodies on update").isEqualTo(1);
        assertThat(artifactBodiesQuery.get(0).getContent()).isEqualTo(newArtifactBody);
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
        assertThat(requirementType.isPresent()).as("requirement type created").isTrue();
        List<Artifact> requirements = artifactRepository.findByProjectAndType(project, requirementType.get());
        assertThat(requirements.size()).as("requirements created").isEqualTo(1);

        // VP - design definitions created
        Optional<ArtifactType> designType = artifactTypeRepository
            .findByProjectAndNameIgnoreCase(project, "design");
        assertThat(designType.isPresent()).as("design type created").isTrue();
        List<Artifact> designs = artifactRepository.findByProjectAndType(project, designType.get());
        assertThat(designs.size())
            .as("designs created)")
            .isEqualTo(1);

        List<Artifact> projectArtifacts = artifactRepository.getProjectArtifacts(project);
        assertThat(projectArtifacts.size()).isEqualTo(N_ARTIFACTS);

        // VP - Artifact bodies
        List<ArtifactBody> artifactBodies = artifactBodyRepository.findByProjectVersion(projectVersion);
        assertThat(artifactBodies.size())
            .as("artifact bodies created")
            .isEqualTo(N_ARTIFACTS);
        List<TraceLink> traceLinks = traceLinkRepository.getApprovedLinks(project);
        assertThat(traceLinks.size()).isEqualTo(N_TRACES);
    }
}
