package features.types;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.UUID;

import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.types.ArtifactType;

import features.base.ApplicationBaseTest;
import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * This tests that client is able to:
 * - create artifact type
 * - receive notification of creation
 * - update artifact type
 * - receive notification of update
 * - delete artifact type
 * - receive notification of deletion
 */
class TestArtifactTypeCRUD extends ApplicationBaseTest {

    String editTypePath = AppRoutes.ArtifactType.CREATE_OR_UPDATE_ARTIFACT_TYPE;

    @Test
    void testCRUD() throws Exception {
        // Step - Create empty project
        Project project = dbEntityBuilder.newProjectWithReturn(projectName);

        // Step - Subscribe to project
        notificationTestService.createNewConnection(defaultUser).subscribeToProject(defaultUser, project);

        // Step - Create artifact type
        ArtifactType initialArtifactType = new ArtifactType(project, TypeConstants.name);
        JSONObject createdType = SafaRequest
            .withRoute(editTypePath)
            .withProject(project)
            .postWithJsonObject(initialArtifactType);

        // VP - Verify that typeId was included in response
        UUID typeId = UUID.fromString(createdType.getString("typeId"));
        assertThat(typeId).isNotNull();

        // VP - Verify that default icon was created
        String icon = createdType.getString("icon");
        assertThat(icon).contains("mdi");

        // VP - Verify that type is persisted
        ArtifactType createdArtifactType = this.artifactTypeRepository.findByTypeId(typeId);
        assertThat(createdArtifactType.getName()).isEqualTo(TypeConstants.name);
        assertThat(createdArtifactType.getIcon()).isEqualTo(icon);

        // VP - Verify that notification received
        EntityChangeMessage creationMessage = notificationTestService.getNextMessage(defaultUser);
        verifyUpdateChange(creationMessage, typeId);

        // Step - Edit ion
        createdArtifactType.setIcon(TypeConstants.newIconName);
        JSONObject updatedType = SafaRequest
            .withRoute(editTypePath)
            .withProject(project)
            .postWithJsonObject(createdArtifactType);

        // VP - Verify that new icon in updated type
        assertThat(updatedType.getString("icon")).isEqualTo(TypeConstants.newIconName);

        // VP - Verify that update icon is persisted
        ArtifactType updatedArtifactType = this.artifactTypeRepository.findByTypeId(typeId);
        assertThat(updatedArtifactType.getIcon()).isEqualTo(TypeConstants.newIconName);

        // VP - Verify that notification of update is received
        EntityChangeMessage updatedMessage = notificationTestService.getNextMessage(defaultUser);
        verifyUpdateChange(updatedMessage, typeId);

        // Step - Retrieve artifact type
        JSONArray projectTypes = SafaRequest
            .withRoute(AppRoutes.ArtifactType.GET_PROJECT_ARTIFACT_TYPES)
            .withProject(project)
            .getWithJsonArray();

        // VP - Verify that type retrieved.
        assertThat(projectTypes.length()).isEqualTo(1);
        assertThat(projectTypes.getJSONObject(0).getString("name")).isEqualTo(TypeConstants.name);

        // Step - Delete artifact type
        SafaRequest
            .withRoute(AppRoutes.ArtifactType.DELETE_ARTIFACT_TYPE)
            .withType(createdArtifactType)
            .deleteWithJsonObject();

        // Step - Retrieve artifact types
        projectTypes = SafaRequest
            .withRoute(AppRoutes.ArtifactType.GET_PROJECT_ARTIFACT_TYPES)
            .withProject(project)
            .getWithJsonArray();

        // VP - Verify that type retrieved.
        assertThat(projectTypes.length()).isZero();

        // VP - Verify that notification of deletion is received
        EntityChangeMessage deletedMessage = notificationTestService.getNextMessage(defaultUser);
        verifyTypeMessage(deletedMessage, typeId, Change.Action.DELETE);
    }

    private void verifyUpdateChange(EntityChangeMessage message, UUID typeId) {
        verifyTypeMessage(message, typeId, Change.Action.UPDATE);
    }

    private void verifyTypeMessage(EntityChangeMessage message, UUID typeId, Change.Action action) {
        assertThat(message.getChanges()).hasSize(1);

        Change change = message.getChanges().get(0);
        assertThat(change.getEntity()).isEqualTo(Change.Entity.TYPES);
        assertThat(change.getAction()).isEqualTo(action);
        assertThat(change.getEntityIds()).hasSize(1).contains(typeId);
    }

    static class TypeConstants {
        public static final String name = "requirement";
        public static final String newIconName = "mdi-something-else";
    }
}
