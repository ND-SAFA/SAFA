package edu.nd.crc.safa.server.db.entities.app;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.server.db.entities.sql.TraceLink;
import edu.nd.crc.safa.server.db.entities.sql.TraceType;

public class TraceApplicationEntity {
    public String traceLinkId;
    public String source;
    public String target;
    public boolean isApproved;
    public double score;
    public TraceType traceType;

    public TraceApplicationEntity() {
    }

    public TraceApplicationEntity(TraceLink trace) {
        this.traceLinkId = trace.getTraceLinkId().toString();
        this.source = trace.getSourceName();
        this.target = trace.getTargetName();
        this.isApproved = trace.getIsApproved();
        this.score = trace.getScore();
        this.traceType = trace.getTraceType();
    }

    public static List<TraceApplicationEntity> createEntities(List<TraceLink> links) {
        return links.stream().map(TraceApplicationEntity::new).collect(Collectors.toList());
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

    public String getTraceLinkId() {
        return traceLinkId;
    }

    public void setTraceLinkId(String traceLinkId) {
        this.traceLinkId = traceLinkId;
    }

    public boolean isApproved() {
        return isApproved;
    }

    public void setApproved(boolean approved) {
        isApproved = approved;
    }

    public double getScore() {
        return score;
    }

    public void setScore(double score) {
        this.score = score;
    }
}
