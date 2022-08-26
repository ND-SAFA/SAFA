package features.notifications.documentartifact;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import builders.CommitBuilder;
import lombok.AllArgsConstructor;
import services.CommitTestService;
import services.MessageVerificationTestService;
import services.NotificationTestService;

@AllArgsConstructor
public class DocumentArtifactNotificationTestService {
    CommitTestService commitService;
    NotificationTestService notificationService;
    MessageVerificationTestService changeMessageVerifies;

    /**
     * Creates project, version, document, and artifact not associated with a document.
     *
     * @throws Exception If server error occurs while creating entities.
     */
    public void createArtifactAndVerifyMessage(ProjectVersion projectVersion,
                                               IDocumentArtifactTest test) throws Exception {
        // Step - Create artifact
        ProjectCommit commit = this.commitService.commit(CommitBuilder
            .withVersion(projectVersion)
            .withAddedArtifact(test.getArtifact()));
        ArtifactAppEntity artifactAdded = commit.getArtifact(ModificationType.ADDED, 0);

        // VP - Verify commit message
        EntityChangeMessage commitMessage = this.notificationService.getNextMessage(test.getShareeEmail());
        this.changeMessageVerifies.verifyArtifactMessage(commitMessage,
            artifactAdded.getId(),
            Change.Action.UPDATE
        );

        // Step - Set current artifact with created id
        test.setArtifact(artifactAdded);
    }
}
