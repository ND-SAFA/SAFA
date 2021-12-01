package unit.messaging;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.api.ProjectWebSocketMessage;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.services.RevisionNotificationService;

import org.junit.jupiter.api.Test;
import unit.WebSocketBaseTest;

/**
 * Tests that uploading flat files incurs a single update message.
 */
public class TestFlatFileMessage extends WebSocketBaseTest {
    @Test
    public void singleMessageOnFlatFileUpload() throws Exception {
        String projectName = "test-project";

        // Step - Create project and version id
        ProjectVersion projectVersion = dbEntityBuilder
            .newProject(currentUser, projectName)
            .newVersionWithReturn(projectName);

        // Step - Connect to websocket listener
        String clientId = "client-one";
        createNewConnection(clientId);

        // Step - Subscribe to project and version topics
        subscribe(clientId, RevisionNotificationService.getVersionTopic(projectVersion));

        // Step - Upload flat files
        uploadFlatFilesToVersion(projectVersion, ProjectPaths.PATH_TO_BEFORE_FILES);

        // VP - Verify that single message sent
        assertThat(getQueueSize(clientId)).isEqualTo(1);
        ProjectWebSocketMessage response = getNextMessage(clientId, ProjectWebSocketMessage.class);
        assertThat(response.getType()).isEqualTo("excluded");
    }
}
