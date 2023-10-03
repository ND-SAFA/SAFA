package edu.nd.crc.safa.test.features.notifications.flatfiles;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.test.features.notifications.AbstractNotificationTest;
import edu.nd.crc.safa.test.requests.FlatFileRequest;

/**
 * Tests that uploading flat files:
 * - incurs a single update message.
 * - update message has single change of type VERSION
 */
public class TestFlatFileProjectUpdateNotificationsCommonRequests extends AbstractNotificationTest {

    private final String parentType = "SafetyRequirement";
    private final String childType = "Requirement";

    @Override
    protected void performAction() throws Exception {
        FlatFileRequest
            .updateProjectVersionFromFlatFiles(
                projectVersion,
                ProjectPaths.Resources.Tests.MINI);
    }

    @Override
    protected void verifyShareeMessage(List<EntityChangeMessage> messages) {
        assertThat(messages).hasSize(4);

        this.rootBuilder
            .verify(v -> v.notifications(n -> n
                .verifyArtifactTypeMessage(messages.get(0), parentType)
                .verifyArtifactTypeMessage(messages.get(1), childType)
                .verifyTraceMatrixMessage(messages.get(2), List.of(childType, parentType))
                .verifyProjectEntitiesMessage(messages.get(3), 2, 1)));
    }
}
