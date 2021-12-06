package edu.nd.crc.safa.server.entities.app;

import edu.nd.crc.safa.server.entities.db.ModificationType;
import edu.nd.crc.safa.server.entities.db.TraceLinkVersion;

public class TraceDelta implements IDeltaEntity {
    ModificationType modificationType;
    TraceAppEntity traceLink;

    public TraceDelta(TraceLinkVersion traceLinkVersion, ModificationType modificationType) {
        this.traceLink = new TraceAppEntity(traceLinkVersion);
        this.modificationType = modificationType;
    }

    public ModificationType getModificationType() {
        return modificationType;
    }

    public void setModificationType(ModificationType modificationType) {
        this.modificationType = modificationType;
    }

    public TraceAppEntity getTraceLink() {
        return traceLink;
    }

    public void setTraceLink(TraceAppEntity traceLink) {
        this.traceLink = traceLink;
    }
}
