package edu.nd.crc.safa.server.entities.app;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.server.entities.db.TraceApproval;
import edu.nd.crc.safa.server.entities.db.TraceLink;
import edu.nd.crc.safa.server.entities.db.TraceType;

import org.json.JSONObject;

/**
 * Represents the front-end model of a trace link.
 */
public class TraceAppEntity {
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
    }

    public TraceAppEntity(String source, String target, double score) {
        this.traceLinkId = "";
        this.source = source;
        this.target = target;
        this.approvalStatus = TraceApproval.UNREVIEWED;
        this.score = score;
        this.traceType = TraceType.GENERATED;
    }

    public TraceAppEntity(TraceLink trace) {
        UUID traceLinkId = trace.getTraceLinkId();
        this.traceLinkId = traceLinkId != null ? traceLinkId.toString() : "";
        this.source = trace.getSourceName();
        this.target = trace.getTargetName();
        this.approvalStatus = trace.getApprovalStatus();
        this.score = trace.getScore();
        this.traceType = trace.getTraceType();
    }

    public static List<TraceAppEntity> createEntities(List<TraceLink> links) {
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
}
