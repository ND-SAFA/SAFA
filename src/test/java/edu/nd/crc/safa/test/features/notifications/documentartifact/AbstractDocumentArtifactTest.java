package edu.nd.crc.safa.test.features.notifications.documentartifact;

import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.test.common.EntityConstants;
import edu.nd.crc.safa.test.features.notifications.documents.TestUpdateDocumentNotification;

public abstract class AbstractDocumentArtifactTest
    extends TestUpdateDocumentNotification implements IDocumentArtifactTest {

    /**
     * ID of artifact being added or removed from document.
     */
    protected UUID artifactId;

    /**
     * Instance of artifact constants.
     */
    protected EntityConstants.ArtifactConstants artifactConstants = new EntityConstants.ArtifactConstants();

    @Override
    public ArtifactAppEntity getArtifact() {
        return this.artifactConstants.artifact;
    }

    @Override
    public void setArtifact(ArtifactAppEntity artifact) {
        this.artifactConstants.artifact.setId(artifact.getId());
        this.artifactId = artifact.getId();
    }
}
