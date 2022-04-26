package edu.nd.crc.safa.server.entities.app.project;

import java.util.Objects;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.server.entities.db.TraceApproval;
import edu.nd.crc.safa.server.entities.db.TraceType;

import org.json.JSONObject;

/**
 * Represents the front-end model of a trace link.
 */
public class TraceAppEntity implements IAppEntity {
    @NotNull
    public String traceLinkId; // TODO: Convert to UUID
    @NotEmpty
    public String sourceName;
    public String sourceId;
    @NotEmpty
    public String targetName;
    public String targetId;
    public TraceApproval approvalStatus;
    public double score;
    public TraceType traceType;

    public TraceAppEntity() {
        this.traceLinkId = "";
    }

    public TraceAppEntity(String traceLinkId,
                          String sourceName,
                          String sourceId,
                          String targetName,
                          String targetId,
                          TraceApproval traceApproval,
                          double score,
                          TraceType traceType) {
        this.traceLinkId = traceLinkId;
        this.sourceName = sourceName;
        this.sourceId = sourceId;
        this.targetName = targetName;
        this.targetId = targetId;
        this.approvalStatus = traceApproval;
        this.score = score;
        this.traceType = traceType;
    }

    public TraceAppEntity asManualTrace() {
        this.setApprovalStatus(TraceApproval.APPROVED);
        this.setScore(1);
        this.setTraceType(TraceType.MANUAL);
        return this;
    }

    public TraceAppEntity asGeneratedTrace(double score) {
        this.setApprovalStatus(TraceApproval.UNREVIEWED);
        this.setScore(score);
        this.setTraceType(TraceType.GENERATED);
        return this;
    }

    public TraceAppEntity betweenArtifacts(String sourceName, String targetName) {
        this.setSourceName(sourceName);
        this.setTargetName(targetName);
        return this;
    }

    public TraceApproval getApprovalStatus() {
        return approvalStatus;
    }

    public void setApprovalStatus(TraceApproval approvalStatus) {
        this.approvalStatus = approvalStatus;
    }

    public TraceType getTraceType() {
        return traceType;
    }

    public void setTraceType(TraceType traceType) {
        this.traceType = traceType;
    }

    public String getSourceId() {
        return sourceId;
    }

    public void setSourceId(String sourceId) {
        this.sourceId = sourceId;
    }

    public String getTargetId() {
        return targetId;
    }

    public void setTargetId(String targetId) {
        this.targetId = targetId;
    }

    public String getSourceName() {
        return this.sourceName;
    }

    public void setSourceName(String sourceName) {
        this.sourceName = sourceName;
    }

    public String getTargetName() {
        return this.targetName;
    }

    public void setTargetName(String targetName) {
        this.targetName = targetName;
    }

    public String getTraceLinkId() {
        return traceLinkId;
    }

    public void setTraceLinkId(String traceLinkId) {
        this.traceLinkId = traceLinkId;
    }

    public double getScore() {
        return score;
    }

    public void setScore(double score) {
        this.score = score;
    }

    public String toString() {
        JSONObject json = new JSONObject();
        json.put("traceLinkId", this.traceLinkId);
        json.put("source", sourceName);
        json.put("target", targetName);
        json.put("type", traceType);
        json.put("status", approvalStatus);
        json.put("score", score);
        return json.toString();
    }

    @Override
    public String getBaseEntityId() {
        return this.traceLinkId;
    }

    @Override
    public void setBaseEntityId(String id) {
        this.traceLinkId = id;
    }

    public boolean equals(TraceAppEntity other) {
        return Objects.equals(this.sourceName, other.sourceName)
            && Objects.equals(this.targetName, other.targetName);
    }
}
