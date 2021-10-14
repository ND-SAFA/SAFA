package edu.nd.crc.safa.warnings;

public class Function {
    public int count;
    public Condition condition;
    public String targetArtifactType;
    public Relationship relationship;
    public String sourceArtifactType;

    public String toString() {
        return String.format("%s->%s %s %d", sourceArtifactType, targetArtifactType, condition, count);
    }
}
