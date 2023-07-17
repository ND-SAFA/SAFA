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
    boolean isVisible = true;

    public TraceAppEntity(String sourceName, String targetName) {
        this.sourceName = sourceName;
        this.targetName = targetName;
    }

    public TraceAppEntity(UUID traceLinkId,
                          String sourceName,
                          UUID sourceId,
                          String targetName,
                          UUID targetId,
                          ApprovalStatus approvalStatus,
                          double score,
                          TraceType traceType,
                          boolean isVisible) {
        this(sourceName, targetName);
        this.score = score;
        this.traceLinkId = traceLinkId;
        this.sourceId = sourceId;
        this.targetId = targetId;
        this.approvalStatus = approvalStatus;
        this.traceType = traceType;
        this.isVisible = isVisible;
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
        this.setVisible(true);
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
