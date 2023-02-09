package edu.nd.crc.safa.test.features.notifications.flatfiles;

import static org.assertj.core.api.Assertions.assertThat;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.test.features.notifications.AbstractNotificationTest;
import edu.nd.crc.safa.test.requests.FlatFileRequest;

/**
 * Tests that uploading flat files:
 * - incurs a single update message.
 * - update message has single change of type VERSION
 */
public class TestUpdateProject extends AbstractNotificationTest {

    @Override
    protected void performAction() throws Exception {
        FlatFileRequest
            .updateProjectVersionFromFlatFiles(
                projectVersion,
                ProjectPaths.Resources.Tests.DefaultProject.V1);
    }

    @Override
    protected void verifyShareeMessage(EntityChangeMessage message) {
        assertThat(message.getChanges())
            .as("single change in message")
            .hasSize(1);

        Change change = message.getChanges().get(0);

        assertThat(change.getEntity())
            .as("change entity is VERSION")
            .isEqualTo(Change.Entity.VERSION);
    }
}
