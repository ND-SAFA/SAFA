package edu.nd.crc.safa.test.features.notifications.documentartifact;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.test.common.IShareTest;

public interface IDocumentArtifactTest extends IShareTest {
    /**
     * Returns artifact to create in pre-test setup.
     *
     * @return {@link ArtifactAppEntity} artifact to create for document test.
     */
    ArtifactAppEntity getArtifact();

    /**
     * Sets the artifacts details for add/remove in document.
     *
     * @param artifact The artifact created to use to add or remove in document.
     */
    void setArtifact(ArtifactAppEntity artifact);
}
