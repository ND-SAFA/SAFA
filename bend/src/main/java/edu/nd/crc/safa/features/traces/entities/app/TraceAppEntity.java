package edu.nd.crc.safa.features.traces.entities.app;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.traces.entities.db.TraceType;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.validation.constraints.NotEmpty;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Represents the front-end model of a trace link.
 */
@NoArgsConstructor
@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class TraceAppEntity implements IAppEntity {
    private UUID traceLinkId;
    @NotEmpty
    private String sourceName;
    private UUID sourceId;
    @NotEmpty
    private String targetName;
    private UUID targetId;
    private ApprovalStatus approvalStatus;
    private double score;
    private TraceType traceType;
    private boolean isVisible = true;
    private String explanation;

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
                          boolean isVisible,
                          String explanation
    ) {
        this(sourceName, targetName);
        this.score = score;
        this.traceLinkId = traceLinkId;
        this.sourceId = sourceId;
        this.targetId = targetId;
        this.approvalStatus = approvalStatus;
        this.traceType = traceType;
        this.isVisible = isVisible;
        this.explanation = explanation;
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

    public TraceAppEntity withExplanation(String explanation) {
        this.explanation = explanation;
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

    @JsonIgnore
    public List<String> getMissingRequiredFields() {
        List<String> missingFields = new ArrayList<>();

        if ((sourceName == null || sourceName.isBlank()) && sourceId == null) {
            missingFields.add("sourceName or sourceId");
        }
        if ((targetName == null || targetName.isBlank()) && targetId == null) {
            missingFields.add("targetName or targetId");
        }

        return missingFields;
    }
}
