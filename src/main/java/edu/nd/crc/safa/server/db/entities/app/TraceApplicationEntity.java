package edu.nd.crc.safa.server.db.entities.app;

import edu.nd.crc.safa.server.db.entities.sql.TraceLink;

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
