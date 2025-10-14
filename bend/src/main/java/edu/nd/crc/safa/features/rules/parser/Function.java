package edu.nd.crc.safa.features.rules.parser;

import lombok.Data;

/**
 * Defines a check between two artifact types containing a source type, target type, and condition that must
 * be met between them.
 */
@Data
public class Function {
    private String targetArtifactType;
    private ArtifactRelationship artifactRelationship;
    private String sourceArtifactType;
    private Condition condition;
    private int count;
}
