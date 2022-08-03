package edu.nd.crc.safa.features.rules.parser;

import lombok.Data;

/**
 * Defines a check between two artifact types containing a source type, target type, and condition that must
 * be met between them.
 */
@Data
public class Function {
    String targetArtifactType;
    ArtifactRelationship artifactRelationship;
    String sourceArtifactType;
    Condition condition;
    int count;
}
