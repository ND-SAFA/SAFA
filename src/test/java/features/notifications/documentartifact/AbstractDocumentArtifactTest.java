package features.notifications.documentartifact;

import java.util.HashMap;
import java.util.UUID;
import javax.annotation.PostConstruct;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;

import features.notifications.documents.TestUpdateDocumentNotification;

public abstract class AbstractDocumentArtifactTest extends TestUpdateDocumentNotification implements IDocumentArtifactTest {
    /**
     * ID of artifact being added or removed from document.
     */
    protected UUID artifactId;

    /**
     * Instance of artifact constants.
     */
    protected ArtifactConstants artifactConstants = new ArtifactConstants();

    /**
     * Test service used to construct project setup.
     */
    protected DocumentArtifactNotificationTestService testService;

    @PostConstruct
    public void initService() {
        this.testService = new DocumentArtifactNotificationTestService(
            this.commitService,
            this.notificationService,
            this.changeMessageVerifies);
    }

    @Override
    public ArtifactAppEntity getArtifact() {
        return this.artifactConstants.artifact;
    }

    @Override
    public void setArtifact(ArtifactAppEntity artifact) {
        this.artifactConstants.artifact.setId(artifact.getId());
        this.artifactId = UUID.fromString(artifact.getId());
    }

    class ArtifactConstants {
        final String type = "Requirement";
        final String name = "R0";
        final String summary = "";
        final String body = "body";
        ArtifactAppEntity artifact = new ArtifactAppEntity(
            "",
            type,
            name,
            summary,
            body,
            DocumentType.ARTIFACT_TREE,
            new HashMap<>()
        );
    }
}
