package edu.nd.crc.safa.warnings;

import lombok.Data;

/**
 * Defines a check between two artifact types containing a source type, target type, and condition that must
 * be met between them.
 */
@Data
public class Function {
    public int count;
    public Condition condition;
    public String targetArtifactType;
    public ArtifactRelationship artifactRelationship;
    public String sourceArtifactType;
}
