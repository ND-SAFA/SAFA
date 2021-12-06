package edu.nd.crc.safa.server.entities.app;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.server.entities.db.TraceApproval;
import edu.nd.crc.safa.server.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.server.entities.db.TraceType;

import org.json.JSONObject;

/**
 * Represents the front-end model of a trace link.
 */
public class TraceAppEntity implements IAppEntity {
    @NotNull
    public String traceLinkId;

    @NotEmpty
    public String source;

    @NotEmpty
    public String target;

    public TraceApproval approvalStatus;

    public double score;

    public TraceType traceType;

    public TraceAppEntity() {
        this.traceLinkId = "";
    }

    public TraceAppEntity(String source, String target) {
        this();
        this.source = source;
        this.target = target;
        this.approvalStatus = TraceApproval.APPROVED;
        this.score = 1;
        this.traceType = TraceType.MANUAL;
    }

    public TraceAppEntity(String source, String target, double score) {
        this();
        this.source = source;
        this.target = target;
        this.approvalStatus = TraceApproval.UNREVIEWED;
        this.score = score;
        this.traceType = TraceType.GENERATED;
    }

    public TraceAppEntity(TraceLinkVersion trace) {
        UUID traceLinkId = trace.getTraceLink().getTraceLinkId();
        this.traceLinkId = traceLinkId != null ? traceLinkId.toString() : "";
        this.source = trace.getTraceLink().getSourceName();
        this.target = trace.getTraceLink().getTargetName();
        this.approvalStatus = trace.getApprovalStatus();
        this.score = trace.getScore();
        this.traceType = trace.getTraceType();
    }

    public static List<TraceAppEntity> createEntities(List<TraceLinkVersion> links) {
        return links.stream().map(TraceAppEntity::new).collect(Collectors.toList());
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

    public TraceApproval isApproved() {
        return approvalStatus;
    }

    public void setApproved(TraceApproval approvalStatus) {
        this.approvalStatus = approvalStatus;
    }

    public double getScore() {
        return score;
    }

    public void setScore(double score) {
        this.score = score;
    }

    public String toString() {
        JSONObject json = new JSONObject();
        json.put("source:", source);
        json.put("target:", target);
        json.put("traceType:", traceType);
        return json.toString();
    }

    @Override
    public String getName() {
        return source + "-" + target;
    }
}
