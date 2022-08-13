package features.artifacts.types;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.UUID;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactType;
import edu.nd.crc.safa.features.notifications.messages.ProjectMessage;
import edu.nd.crc.safa.features.projects.entities.app.ProjectEntityTypes;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import features.base.ApplicationBaseTest;
import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * This tests that endpoints are able to create and update artifact types.
 */
class TestCrudSingleType extends ApplicationBaseTest {

    @Test
    void testCreateArtifactType() throws Exception {
        String projectName = "project-name";
        String typeName = "requirement";

        // Step - Create empty project
        Project project = dbEntityBuilder
            .newProjectWithReturn(projectName);

        // Step - Subscribe to project
        createNewConnection(defaultUser).subscribeToProject(defaultUser, project);

        // Step - Create artifact type
        String endpoint = RouteBuilder
            .withRoute(AppRoutes.Projects.ArtifactType.CREATE_OR_UPDATE_ARTIFACT_TYPE)
            .withProject(project)
            .buildEndpoint();
        ArtifactType initialArtifactType = new ArtifactType(project, typeName);
        JSONObject createdType = SafaRequest
            .withRoute(endpoint)
            .postWithJsonObject(initialArtifactType,
                status().is2xxSuccessful());

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
        ProjectMessage projectMessage = getNextMessage(defaultUser, ProjectMessage.class);
        assertThat(projectMessage.getUser()).isEqualTo(defaultUser);
        assertThat(projectMessage.getType()).isEqualTo(ProjectEntityTypes.TYPES);

        // Step - Edit artifact type
        String newIconName = "mdi-something-else";
        createdArtifactType.setIcon(newIconName);
        JSONObject updatedType = SafaRequest
            .withRoute(endpoint)
            .postWithJsonObject(createdArtifactType,
                status().is2xxSuccessful());

        // VP - Verify that change is made
        assertThat(updatedType.getString("icon")).isEqualTo(newIconName);

        // VP - Verify that update is persisted
        ArtifactType updatedArtifactType = this.artifactTypeRepository.findByTypeId(UUID.fromString(typeId));
        assertThat(updatedArtifactType.getIcon()).isEqualTo(newIconName);

        // VP - Verify that notification of update is received
        projectMessage = getNextMessage(defaultUser, ProjectMessage.class);
        assertThat(projectMessage.getUser()).isEqualTo(defaultUser);
        assertThat(projectMessage.getType()).isEqualTo(ProjectEntityTypes.TYPES);

        // Step - Retrieve artifact type
        JSONArray projectTypes = SafaRequest
            .withRoute(AppRoutes.Projects.ArtifactType.GET_PROJECT_ARTIFACT_TYPES)
            .withProject(project)
            .getWithJsonArray();

        // VP - Verify that type retrieved.
        assertThat(projectTypes.length()).isEqualTo(1);
        assertThat(projectTypes.getJSONObject(0).getString("name")).isEqualTo(typeName);

        // Step - Delete artifact type
        SafaRequest
            .withRoute(AppRoutes.Projects.ArtifactType.DELETE_ARTIFACT_TYPE)
            .withType(createdArtifactType)
            .deleteWithJsonObject();

        // Step - Retrieve artifact types
        projectTypes = SafaRequest
            .withRoute(AppRoutes.Projects.ArtifactType.GET_PROJECT_ARTIFACT_TYPES)
            .withProject(project).getWithJsonArray();

        // VP - Verify that type retrieved.
        assertThat(projectTypes.length()).isZero();

        // VP - Verify that notification of deletion is received
        projectMessage = getNextMessage(defaultUser, ProjectMessage.class);
        assertThat(projectMessage.getUser()).isEqualTo(defaultUser);
        assertThat(projectMessage.getType()).isEqualTo(ProjectEntityTypes.TYPES);
    }
}
