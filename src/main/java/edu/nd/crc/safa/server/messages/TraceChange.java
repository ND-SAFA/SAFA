package edu.nd.crc.safa.server.messages;

import edu.nd.crc.safa.server.db.entities.app.TraceApplicationEntity;
import edu.nd.crc.safa.server.db.entities.sql.ModificationType;

public class TraceChange {
    ModificationType revisionType;
    TraceApplicationEntity trace;

    public TraceChange() {
    }

    public TraceChange(ModificationType revisionType, TraceApplicationEntity trace) {
    }

    public ModificationType getRevisionType() {
        return revisionType;
    }

    public void setRevisionType(ModificationType revisionType) {
        this.revisionType = revisionType;
    }

    public TraceApplicationEntity getTrace() {
        return trace;
    }

    public void setTrace(TraceApplicationEntity trace) {
        this.trace = trace;
    }
}
