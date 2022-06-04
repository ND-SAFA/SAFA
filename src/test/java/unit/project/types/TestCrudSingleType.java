package unit.project.types;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.UUID;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.app.project.ProjectEntityTypes;
import edu.nd.crc.safa.server.entities.app.project.ProjectMessage;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.Project;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

/**
 * This tests that endpoints are able to create and update artifact types.
 */
public class TestCrudSingleType extends ApplicationBaseTest {

    @Test
    public void testCreateArtifactType() throws Exception {
        String projectName = "project-name";
        String typeName = "requirement";

        // Step - Create empty project
        Project project = dbEntityBuilder
            .newProjectWithReturn(projectName);

        // Step - Subscribe to project
        createNewConnection(currentUsername).subscribeToProject(currentUsername, project);

        // Step - Create artifact type
        String endpoint = RouteBuilder
            .withRoute(AppRoutes.Projects.ArtifactType.createOrUpdateArtifactType)
            .withProject(project)
            .get();
        ArtifactType initialArtifactType = new ArtifactType(project, typeName);
        JSONObject createdType = sendPost(endpoint, toJson(initialArtifactType), status().is2xxSuccessful());

        // VP - Verify that id is returned and icon is established.
        String typeId = createdType.getString("typeId");
        String icon = createdType.getString("icon");
        assertThat(typeId).isNotEmpty();
        assertThat(icon).contains("mdi");

        // VP - Verify that type is persisted
        ArtifactType createdArtifactType = this.artifactTypeRepository.findByTypeId(UUID.fromString(typeId));
        assertThat(createdArtifactType.getName()).isEqualTo(typeName);
        assertThat(createdArtifactType.getIcon()).isEqualTo(icon);

        // VP - Verify that notification received
        ProjectMessage projectMessage = getNextMessage(currentUsername, ProjectMessage.class);
        assertThat(projectMessage.getUser()).isEqualTo(currentUsername);
        assertThat(projectMessage.getType()).isEqualTo(ProjectEntityTypes.TYPES);

        // Step - Edit artifact type
        String newIconName = "mdi-something-else";
        createdArtifactType.setIcon(newIconName);
        JSONObject updatedType = sendPost(endpoint, toJson(createdArtifactType), status().is2xxSuccessful());

        // VP - Verify that change is made
        assertThat(updatedType.getString("icon")).isEqualTo(newIconName);

        // VP - Verify that update is persisted
        ArtifactType updatedArtifactType = this.artifactTypeRepository.findByTypeId(UUID.fromString(typeId));
        assertThat(updatedArtifactType.getIcon()).isEqualTo(newIconName);

        // VP - Verify that notification of update is received
        projectMessage = getNextMessage(currentUsername, ProjectMessage.class);
        assertThat(projectMessage.getUser()).isEqualTo(currentUsername);
        assertThat(projectMessage.getType()).isEqualTo(ProjectEntityTypes.TYPES);

        // Step - Retrieve artifact type
        String getEndpoint = RouteBuilder
            .withRoute(AppRoutes.Projects.ArtifactType.getProjectArtifactTypes)
            .withProject(project)
            .get();
        JSONArray projectTypes = sendGetWithArrayResponse(getEndpoint, status().is2xxSuccessful());

        // VP - Verify that type retrieved.
        assertThat(projectTypes.length()).isEqualTo(1);
        assertThat(projectTypes.getJSONObject(0).getString("name")).isEqualTo(typeName);

        // Step - Delete artifact type
        String deleteEndpoint = RouteBuilder
            .withRoute(AppRoutes.Projects.ArtifactType.deleteArtifactType)
            .withType(createdArtifactType)
            .get();
        sendDelete(deleteEndpoint, status().is2xxSuccessful());

        // Step - Retrieve artifact types
        projectTypes = sendGetWithArrayResponse(getEndpoint, status().is2xxSuccessful());

        // VP - Verify that type retrieved.
        assertThat(projectTypes.length()).isEqualTo(0);

        // VP - Verify that notification of deletion is received
        projectMessage = getNextMessage(currentUsername, ProjectMessage.class);
        assertThat(projectMessage.getUser()).isEqualTo(currentUsername);
        assertThat(projectMessage.getType()).isEqualTo(ProjectEntityTypes.TYPES);
    }
}
