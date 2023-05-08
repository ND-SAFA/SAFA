package edu.nd.crc.safa.features.summary;

import lombok.Data;

enum TGenSummaryArtifactType {
    /**
     * Identifies natural language artifacts.
     */
    NL,
    /**
     * Identifies python files.
     */
    PY,
    /**
     * Identifies java files.
     */
    JAVA
}

@Data
class TGenSummaryArtifact {
    /**
     * The content to summarize.
     */
    String content;
    /**
     * The type of summarization.
     */
    TGenSummaryArtifactType type = TGenSummaryArtifactType.NL;
}
