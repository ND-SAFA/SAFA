package unit.messaging;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.app.project.VersionEntityTypes;
import edu.nd.crc.safa.server.entities.app.project.VersionMessage;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

/**
 * Tests that uploading flat files incurs a single update message.
 */
public class TestFlatFileMessage extends ApplicationBaseTest {
    @Test
    public void singleMessageOnFlatFileUpload() throws Exception {
        String projectName = "test-project";

        // Step - Create project and version id
        ProjectVersion projectVersion = dbEntityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);

        // Step - Connect to websocket and subscribe to version messages.
        String clientId = "client-one";
        createNewConnection(clientId).subscribeToVersion(clientId, projectVersion);

        // Step - Upload flat files
        uploadFlatFilesToVersion(projectVersion, ProjectPaths.PATH_TO_DEFAULT_PROJECT);

        // VP - Verify that single message sent
        assertThat(getQueueSize(clientId)).isEqualTo(1);
        VersionMessage message = getNextMessage(clientId, VersionMessage.class);
        assertThat(message.getType()).isEqualTo(VersionEntityTypes.VERSION);
    }
}
