package unit.messaging;

import static org.assertj.core.api.Assertions.assertThat;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.messages.Revision;

import org.junit.jupiter.api.Test;
import unit.TestConstants;
import unit.WebSocketBaseTest;

public class TestClientsCanSendAndReceive extends WebSocketBaseTest {

    @Test
    public void canSendAndReceiveMessagesBetweenClients() throws Exception {
        String projectName = "websocket-test";
        String clientOne = "user-1";
        String clientTwo = "user-2";

        // Step - Create project version to collaborate on
        ProjectVersion projectVersion = entityBuilder
            .newProject(projectName)
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
        assertThat(getQueueSize(clientOne)).isGreaterThan(2);
        assertThat(getQueueSize(clientTwo)).isGreaterThan(2);

        // Step - Read message
        Revision clientOneRevision = getNextMessage(clientOne, Revision.class);
        Revision clientTwoRevision = getNextMessage(clientTwo, Revision.class);

        // VP - Verify that message sent is received
        assertThat(clientOneRevision.getArtifactChanges().size()).isEqualTo(TestConstants.N_ARTIFACTS);
        assertThat(clientTwoRevision.getArtifactChanges().size()).isEqualTo(TestConstants.N_ARTIFACTS);
    }
}
