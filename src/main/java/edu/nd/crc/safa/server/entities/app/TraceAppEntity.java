package edu.nd.crc.safa.server.entities.app;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.server.entities.db.Artifact;
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

    public TraceAppEntity(String sourceName, String targetName) {
        this();
        this.sourceName = sourceName;
        this.targetName = targetName;
        this.approvalStatus = TraceApproval.APPROVED;
        this.score = 1;
        this.traceType = TraceType.MANUAL;
    }

    public TraceAppEntity(String sourceName, String targetName, double score) {
        this();
        this.sourceName = sourceName;
        this.targetName = targetName;
        this.approvalStatus = TraceApproval.UNREVIEWED;
        this.score = score;
        this.traceType = TraceType.GENERATED;
    }

    public TraceAppEntity(TraceLinkVersion trace) {
        UUID traceLinkId = trace.getTraceLink().getTraceLinkId();
        Artifact sourceArtifact = trace.getTraceLink().getSourceArtifact();
        Artifact targetArtifact = trace.getTraceLink().getTargetArtifact();

        this.traceLinkId = traceLinkId != null ? traceLinkId.toString() : "";
        this.sourceName = sourceArtifact.getName();
        this.sourceId = sourceArtifact.getArtifactId().toString();
        this.targetName = targetArtifact.getName();
        this.targetId = targetArtifact.getArtifactId().toString();
        this.approvalStatus = trace.getApprovalStatus();
        this.score = trace.getScore();
        this.traceType = trace.getTraceType();
    }

    public static List<TraceAppEntity> createEntities(List<TraceLinkVersion> links) {
        return links.stream().map(TraceAppEntity::new).collect(Collectors.toList());
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
        json.put("source", sourceName);
        json.put("target", targetName);
        json.put("type", traceType);
        json.put("status", approvalStatus);
        json.put("score", score);
        return json.toString();
    }

    @Override
    public String getId() {
        return this.traceLinkId;
    }

    @Override
    public void setId(String id) {
        this.traceLinkId = id;
    }

    public boolean equals(TraceAppEntity other) {
        return this.sourceName == other.sourceName && this.targetName == other.targetName;
    }
}
