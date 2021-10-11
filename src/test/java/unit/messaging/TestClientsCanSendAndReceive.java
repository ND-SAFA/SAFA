package unit.messaging;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.ArrayList;

import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.messages.Revision;

import org.junit.jupiter.api.Test;
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

        // Step - Create two client and subscript to version
        String topicSubscriptionDestination = String.format("/topic/revisions/%s", versionId);
        createNewConnection(clientOne)
            .subscribe(clientOne, topicSubscriptionDestination);
        createNewConnection(clientTwo)
            .subscribe(clientTwo, topicSubscriptionDestination);

        // Step - Create revision class and send over line
        int revisionNumber = projectVersion.getRevision();
        Revision revision = new Revision(revisionNumber, new ArrayList<>(), new ArrayList<>());
        String revisionDestination = String.format("/app/revisions/%s", versionId);
        sendMessage(clientOne, revisionDestination, revision);

        // Step - Read message
        Revision localRevision = getNextMessage(clientOne, Revision.class);
        Revision externalRevision = getNextMessage(clientTwo, Revision.class);

        // VP - Verify that message sent is received
        assertThat(localRevision.getRevision()).isEqualTo(revisionNumber);
        assertThat(externalRevision.getRevision()).isEqualTo(revisionNumber);
    }
}
