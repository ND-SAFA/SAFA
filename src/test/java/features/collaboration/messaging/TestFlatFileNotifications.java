package features.collaboration.messaging;

import static org.assertj.core.api.Assertions.assertThat;

import features.base.ApplicationBaseTest;
import org.junit.jupiter.api.Test;
import edu.nd.crc.safa.builders.requests.FlatFileRequest;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;



/**
 * Tests that uploading flat files:
 * - incurs a single update message.
 * - update message has single change of type VERSION
 */
class TestFlatFileNotifications extends ApplicationBaseTest {
    String clientId = "client-one";

    @Test
    void singleNotificationOnUpload() throws Exception {
        // Step - Create project and version id
        ProjectVersion projectVersion = dbEntityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);

        // Step - Subscribe to version notifications
        notificationTestService.createNewConnection(clientId).subscribeToVersion(clientId, projectVersion);

        // Step - Upload flat files
        FlatFileRequest.updateProjectVersionFromFlatFiles(projectVersion, ProjectPaths.Tests.DefaultProject.V1);

        // VP - Verify that single message sent
        assertThat(notificationTestService.getQueueSize(clientId)).isEqualTo(1);
        EntityChangeMessage message = notificationTestService.getNextMessage(clientId);
        assertThat(message.getChanges()).hasSize(1);

        // VP - Verify that entity changed = VERSIONS
        Change change = message.getChanges().get(0);
        assertThat(change.getEntity()).isEqualTo(Change.Entity.VERSION);
    }
}
