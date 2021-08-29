package edu.nd.crc.safa.entities.application;

import edu.nd.crc.safa.entities.database.TraceLink;

public class TraceApplicationEntity {
    public String source;
    public String target;

    public TraceApplicationEntity() {
    }

    public TraceApplicationEntity(TraceLink trace) {
        this.source = trace.getSourceName();
        this.target = trace.getTargetName();
    }

    public String getSource() {
        return this.source;
    }

    public void setSource(String source) {
        this.source = source;
    }

    public String getTarget() {
        return this.target;
    }

    public void setTarget(String target) {
        this.target = target;
    }
}
