package edu.nd.crc.safa.test.features.sync;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Test that correct entities are retrived for an EntityChangeMessage
 */
public abstract class AbstractSyncTest extends ApplicationBaseTest {
    /**
     * Converts JSON response to {@link ProjectAppEntity}
     */
    private final ObjectMapper objectMapper = new ObjectMapper();
    /**
     * Project created.
     */
    protected ProjectVersion projectVersion;

    @Test
    public void runTest() throws Exception {
        // Step - Create project and version
        this.projectVersion = this.creationService.createProjectWithNewVersion(projectName);

        // Step - Subscribe user to version
        this.notificationService
            .createNewConnection(defaultUser)
            .subscribeToVersion(defaultUser, projectVersion);

        // Step - Perform action on project
        this.performAction();

        // VP - Verify correctness of message
        EntityChangeMessage actionMessage = this.notificationService.getNextMessage(defaultUser);
        this.verifyActionMessage(actionMessage);

        // Step - Execute sync call
        JSONObject response = SafaRequest
            .withRoute(AppRoutes.Sync.GET_CHANGES)
            .withVersion(this.projectVersion)
            .postWithJsonObject(actionMessage);
        ProjectAppEntity project = this.objectMapper.readValue(response.toString(), ProjectAppEntity.class);

        // VP - Verify project entities
        this.verifyChanges(project);
    }

    abstract void performAction() throws Exception;

    /**
     * Verifies that message is correct as a result of action.
     *
     * @param message The notification sent after action
     */
    abstract void verifyActionMessage(EntityChangeMessage message);

    /**
     * Verifies that entities retrieved from message are accurate.
     *
     * @param project The project entity with the changes
     */
    abstract void verifyChanges(ProjectAppEntity project);
}
