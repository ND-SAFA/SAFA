package edu.nd.crc.safa.warnings;

/**
 * Defines a check between two artifact types containing a source type, target type, and condition that must
 * be met between them.
 */
public class Function {
    public int count;
    public Condition condition;
    public String targetArtifactType;
    public ArtifactRelationship artifactRelationship;
    public String sourceArtifactType;

    public String toString() {
        return String.format("%s->%s %s %d", sourceArtifactType, targetArtifactType, condition, count);
    }
}
