package edu.nd.crc.safa.server.messages;

import edu.nd.crc.safa.server.entities.app.TraceApplicationEntity;
import edu.nd.crc.safa.server.entities.db.ModificationType;

import org.json.JSONObject;

public class TraceChange {
    ModificationType revisionType;
    TraceApplicationEntity trace;

    public TraceChange() {
    }

    public TraceChange(ModificationType revisionType, TraceApplicationEntity trace) {
        this.revisionType = revisionType;
        this.trace = trace;
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

    public String toString() {
        JSONObject json = new JSONObject();
        json.put("Mod:", revisionType);
        json.put("trace:", trace);
        return json.toString();
    }
}
