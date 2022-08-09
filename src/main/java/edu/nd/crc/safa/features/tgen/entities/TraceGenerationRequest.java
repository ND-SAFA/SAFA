package edu.nd.crc.safa.features.tgen.entities;

/**
 * Represents a request to generate links between two artifact types;
 */
public class TraceGenerationRequest {
    String source;
    String target;

    public TraceGenerationRequest() {
    }

    public TraceGenerationRequest(String source, String target) {
        this.source = source;
        this.target = target;
    }

    public String getSource() {
        return source;
    }

    public void setSource(String source) {
        this.source = source;
    }

    public String getTarget() {
        return target;
    }

    public void setTarget(String target) {
        this.target = target;
    }
}
