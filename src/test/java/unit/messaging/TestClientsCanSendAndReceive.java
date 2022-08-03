package unit.messaging;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.builders.requests.FlatFileRequest;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

/**
 * Provides a smoke test verifying that two users subscribed to the same version channel
 * are able to receive updates when the other commits them.
 */
class TestClientsCanSendAndReceive extends ApplicationBaseTest {

    @Test
    void canSendAndReceiveMessagesBetweenClients() throws Exception {
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
        FlatFileRequest.updateProjectVersionFromFlatFiles(projectVersion, ProjectPaths.PATH_TO_DEFAULT_PROJECT);

        // VP - Artifact and traces received
        assertThat(getQueueSize(clientOne)).isEqualTo(1);
        assertThat(getQueueSize(clientTwo)).isEqualTo(1);
    }
}
