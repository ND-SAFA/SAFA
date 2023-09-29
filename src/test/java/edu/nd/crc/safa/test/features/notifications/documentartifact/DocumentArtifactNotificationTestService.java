package edu.nd.crc.safa.test.features.notifications.documentartifact;

import java.util.List;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.entities.NotificationEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.builders.CommitBuilder;
import edu.nd.crc.safa.test.services.AssertionTestService;
import edu.nd.crc.safa.test.services.CommitTestService;
import edu.nd.crc.safa.test.services.MessageVerificationTestService;
import edu.nd.crc.safa.test.services.notifications.NotificationTestService;

import lombok.AllArgsConstructor;

@AllArgsConstructor
public class DocumentArtifactNotificationTestService {
    CommitTestService commitService;
    NotificationTestService notificationService;
    MessageVerificationTestService changeMessageVerifies;
    AssertionTestService assertionService;

    /**
     * Creates project, version, document, and artifact not associated with a document.
     *
     * @param projectVersion The project version to put the artifact in
     * @param test           Contains the artifact and email
     * @throws Exception If server error occurs while creating entities.
     */
    public void createArtifactAndVerifyMessage(ProjectVersion projectVersion,
                                               IDocumentArtifactTest test) throws Exception {
        // Step - Create artifact
        ArtifactAppEntity artifact = test.getArtifact();
        ProjectCommitDefinition commit = this.commitService.commit(CommitBuilder
            .withVersion(projectVersion)
            .withAddedArtifact(artifact));
        ArtifactAppEntity artifactAdded = commit.getArtifact(ModificationType.ADDED, 0);

        // VP - Verify commit message
        List<EntityChangeMessage> commitMessages = this.notificationService.getMessages(test.getSharee());

        this.assertionService.verifyArtifactTypeMessage(commitMessages.get(0), artifact.getType());
        this.assertionService.verifySingleEntityChanges(commitMessages.get(1), List.of(NotificationEntity.ARTIFACTS,
            NotificationEntity.WARNINGS), List.of(1, 0));

        // Step - Set current artifact with created id
        test.setArtifact(artifactAdded);
    }
}
