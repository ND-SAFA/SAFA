package edu.nd.crc.safa.server.messages;

import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.db.ModificationType;

public class ArtifactChange {
    ModificationType revisionType;
    ArtifactAppEntity artifact;

    public ArtifactChange() {
    }

    public ArtifactChange(ModificationType revisionType,
                          ArtifactAppEntity artifact) {
        this.revisionType = revisionType;
        this.artifact = artifact;
    }

    public ModificationType getRevisionType() {
        return revisionType;
    }

    public void setRevisionType(ModificationType revisionType) {
        this.revisionType = revisionType;
    }

    public ArtifactAppEntity getArtifact() {
        return artifact;
    }

    public void setArtifact(ArtifactAppEntity artifact) {
        this.artifact = artifact;
    }
}
