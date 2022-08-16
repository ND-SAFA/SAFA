package edu.nd.crc.safa.features.traces.entities.app;

import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.traces.entities.db.TraceType;

import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Represents the front-end model of a trace link.
 */
@NoArgsConstructor
@Data
public class TraceAppEntity implements IAppEntity {
    @NotNull
    String traceLinkId = "";
    @NotEmpty
    String sourceName;
    String sourceId;
    @NotEmpty
    String targetName;
    String targetId;
    ApprovalStatus approvalStatus;
    double score;
    TraceType traceType;

    public TraceAppEntity(String traceLinkId,
                          String sourceName,
                          String sourceId,
                          String targetName,
                          String targetId,
                          ApprovalStatus approvalStatus,
                          double score,
                          TraceType traceType) {
        this.traceLinkId = traceLinkId;
        this.sourceName = sourceName;
        this.sourceId = sourceId;
        this.targetName = targetName;
        this.targetId = targetId;
        this.approvalStatus = approvalStatus;
        this.score = score;
        this.traceType = traceType;
    }

    public TraceAppEntity asManualTrace() {
        this.setApprovalStatus(ApprovalStatus.APPROVED);
        this.setScore(1);
        this.setTraceType(TraceType.MANUAL);
        return this;
    }

    public TraceAppEntity asGeneratedTrace(double score) {
        this.setApprovalStatus(ApprovalStatus.UNREVIEWED);
        this.setScore(score);
        this.setTraceType(TraceType.GENERATED);
        return this;
    }

    public TraceAppEntity betweenArtifacts(String sourceName, String targetName) {
        this.setSourceName(sourceName);
        this.setTargetName(targetName);
        return this;
    }

    @Override
    public String getBaseEntityId() {
        return this.traceLinkId;
    }

    @Override
    public void setBaseEntityId(String id) {
        this.traceLinkId = id;
    }
}
