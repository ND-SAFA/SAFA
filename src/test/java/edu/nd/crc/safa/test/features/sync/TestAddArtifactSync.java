package edu.nd.crc.safa.test.features.sync;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.entities.NotificationAction;
import edu.nd.crc.safa.test.common.EntityConstants;
import edu.nd.crc.safa.test.services.builders.CommitBuilder;

public class TestAddArtifactSync extends AbstractSyncTest {
    private final EntityConstants.ArtifactConstants artifactConstants = new EntityConstants.ArtifactConstants();
    private UUID artifactId;

    @Override
    void performAction() throws Exception {
        ProjectCommitDefinition projectCommitDefinition = this.commitService.commit(CommitBuilder
            .withVersion(this.projectVersion)
            .withAddedArtifact(artifactConstants.artifact));
        this.artifactId = projectCommitDefinition.getArtifact(ModificationType.ADDED, 0).getId();
    }

    @Override
    void verifyActionMessage(List<EntityChangeMessage> messages) {
        assertThat(messages).hasSize(2);
        EntityChangeMessage message = messages.get(1);
        this.messageVerificationService.verifyArtifactMessage(
            message,
            this.artifactId,
            NotificationAction.UPDATE);
        this.messageVerificationService.verifyWarningMessage(message);
        this.messageVerificationService.verifyUpdateLayout(message, true);
        message.getChanges().forEach(c -> {
            c.getEntities().forEach(e -> {
                if (e instanceof ArtifactAppEntity artifact) {
                    UUID artifactId = artifact.getId();
                    c.getEntityIds().add(artifactId);
                }
            });
        });
    }
}
