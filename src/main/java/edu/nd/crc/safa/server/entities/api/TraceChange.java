package edu.nd.crc.safa.server.entities.api;

import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.ModificationType;

import org.json.JSONObject;

public class TraceChange {
    ModificationType revisionType;
    TraceAppEntity trace;

    public TraceChange() {
    }

    public TraceChange(ModificationType revisionType, TraceAppEntity trace) {
        this.revisionType = revisionType;
        this.trace = trace;
    }

    public ModificationType getRevisionType() {
        return revisionType;
    }

    public void setRevisionType(ModificationType revisionType) {
        this.revisionType = revisionType;
    }

    public TraceAppEntity getTrace() {
        return trace;
    }

    public void setTrace(TraceAppEntity trace) {
        this.trace = trace;
    }

    public String toString() {
        JSONObject json = new JSONObject();
        json.put("Mod:", revisionType);
        json.put("trace:", trace);
        return json.toString();
    }
}
