package unit.messaging;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.common.ProjectPaths;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

/**
 * Provides a smoke test verifying that two users subscribed to the same version channel
 * are able to receive updates when the other commits them.
 */
public class TestClientsCanSendAndReceive extends ApplicationBaseTest {

    @Test
    public void canSendAndReceiveMessagesBetweenClients() throws Exception {
        String projectName = "websocket-test";
        String clientOne = "user-1";
        String clientTwo = "user-2";

        // Step - Create project version to collaborate on
        ProjectVersion projectVersion = dbEntityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);
        Project project = projectVersion.getProject();

        // Step - Create two client and subscript to version
        createNewConnection(clientOne)
            .subscribeToProject(clientOne, project)
            .subscribeToVersion(clientOne, projectVersion);
        createNewConnection(clientTwo)
            .subscribeToProject(clientTwo, project)
            .subscribeToVersion(clientTwo, projectVersion);

        // Step - Upload flat files
        this.uploadFlatFilesToVersion(projectVersion, ProjectPaths.PATH_TO_BEFORE_FILES);

        // VP - Artifact and traces received
        assertThat(getQueueSize(clientOne)).isEqualTo(1);
        assertThat(getQueueSize(clientTwo)).isEqualTo(1);
    }
}
