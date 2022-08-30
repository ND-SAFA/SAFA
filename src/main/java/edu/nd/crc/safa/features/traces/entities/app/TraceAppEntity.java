package edu.nd.crc.safa.features.traces.entities.app;

import java.util.UUID;
import javax.validation.constraints.NotEmpty;

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
    UUID traceLinkId;
    @NotEmpty
    String sourceName;
    UUID sourceId;
    @NotEmpty
    String targetName;
    UUID targetId;
    ApprovalStatus approvalStatus;
    double score;
    TraceType traceType;

    public TraceAppEntity(UUID traceLinkId,
                          String sourceName,
                          UUID sourceId,
                          String targetName,
                          UUID targetId,
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
    public UUID getId() {
        return this.traceLinkId;
    }

    @Override
    public void setId(UUID id) {
        this.traceLinkId = id;
    }
}
