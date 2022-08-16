package features.collaboration.messaging;

import static org.assertj.core.api.Assertions.assertThat;

import edu.nd.crc.safa.builders.requests.FlatFileRequest;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.notifications.entities.old.VersionMessage;
import edu.nd.crc.safa.features.versions.entities.app.VersionEntityTypes;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import features.base.ApplicationBaseTest;
import org.junit.jupiter.api.Test;

/**
 * Tests that uploading flat files incurs a single update message.
 */
class TestFlatFileMessage extends ApplicationBaseTest {
    @Test
    void singleMessageOnFlatFileUpload() throws Exception {
        String projectName = "test-project";

        // Step - Create project and version id
        ProjectVersion projectVersion = dbEntityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);

        // Step - Connect to websocket and subscribe to version messages.
        String clientId = "client-one";
        createNewConnection(clientId).subscribeToVersion(clientId, projectVersion);

        // Step - Upload flat files
        FlatFileRequest.updateProjectVersionFromFlatFiles(projectVersion, ProjectPaths.Tests.DefaultProject.V1);

        // VP - Verify that single message sent
        assertThat(getQueueSize(clientId)).isEqualTo(1);
        VersionMessage message = getNextMessage(clientId, VersionMessage.class);
        assertThat(message.getType()).isEqualTo(VersionEntityTypes.VERSION);
    }
}
