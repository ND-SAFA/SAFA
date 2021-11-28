package unit.messaging;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.junit.jupiter.api.Test;
import unit.WebSocketBaseTest;

/**
 * Provides a smoke test verifying that two users subscribed to the same version channel
 * are able to receive updates when the other commits them.
 */
public class TestClientsCanSendAndReceive extends WebSocketBaseTest {

    @Test
    public void canSendAndReceiveMessagesBetweenClients() throws Exception {
        String projectName = "websocket-test";
        String clientOne = "user-1";
        String clientTwo = "user-2";

        // Step - Create project version to collaborate on
        ProjectVersion projectVersion = dbEntityBuilder
            .newProject(user, projectName)
            .newVersionWithReturn(projectName);
        String versionId = projectVersion.getVersionId().toString();
        String projectId = projectVersion.getProject().getProjectId().toString();

        // Step - Create two client and subscript to version
        String topicSubscriptionDestination = String.format("/topic/revisions/%s", versionId);
        String projectSubscriptionDestination = String.format("/topic/projects/%s", projectId);
        createNewConnection(clientOne)
            .subscribe(clientOne, topicSubscriptionDestination)
            .subscribe(clientOne, projectSubscriptionDestination);
        createNewConnection(clientTwo)
            .subscribe(clientTwo, topicSubscriptionDestination)
            .subscribe(clientTwo, projectSubscriptionDestination);

        // Step - Upload flat files
        this.uploadFlatFilesToVersion(projectVersion, ProjectPaths.PATH_TO_BEFORE_FILES);

        // VP - Artifact and traces received
        assertThat(getQueueSize(clientOne)).isEqualTo(1);
        assertThat(getQueueSize(clientTwo)).isEqualTo(1);
    }
}
