package edu.nd.crc.safa.server.entities.db;

import java.io.Serializable;
import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;
import javax.persistence.UniqueConstraint;

import edu.nd.crc.safa.server.entities.app.TraceAppEntity;

import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;
import org.json.JSONObject;

/**
 * Responsible for marking each trace link in each project.
 */
@Entity
@Table(name = "trace_link",
    uniqueConstraints = {
        @UniqueConstraint(columnNames = {
            "source_artifact_id", "target_artifact_id"
        }, name = "SINGLE_TRACE_BETWEEN_SOURCE_AND_TARGET")
    }
)
public class TraceLink implements Serializable {

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "trace_link_id")
    UUID traceLinkId;
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "source_artifact_id",
        referencedColumnName = "artifact_id",
        nullable = false
    )
    Artifact sourceArtifact;
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "target_artifact_id",
        referencedColumnName = "artifact_id",
        nullable = false
    )
    Artifact targetArtifact;

    @Column(name = "trace_type", nullable = false)
    @Enumerated(EnumType.ORDINAL)
    TraceType traceType;

    @Column(name = "approved")
    TraceApproval approvalStatus;

    @Column(name = "score")
    double score;

    public TraceLink() {
        this.approvalStatus = TraceApproval.UNREVIEWED;
        this.score = 0;
    }

    public TraceLink(TraceAppEntity traceLink) {
        this();
        this.traceType = traceLink.traceType == null ? TraceType.MANUAL : traceLink.traceType;
        this.approvalStatus = traceLink.approvalStatus == null ? getDefaultApprovalStatus(this.traceType) :
            traceLink.approvalStatus;
        this.score = traceLink.score == 0 ? this.score : traceLink.score;
        if (traceLink.getTraceLinkId() != null) {
            this.traceLinkId = UUID.fromString(traceLink.getTraceLinkId());
        }
    }

    public TraceLink(Artifact sourceArtifact,
                     Artifact targetArtifact) {
        this();
        this.sourceArtifact = sourceArtifact;
        this.targetArtifact = targetArtifact;
        setIsManual();
    }

    public TraceLink(Artifact sourceArtifact,
                     Artifact targetArtifact,
                     double score) {
        this();
        this.sourceArtifact = sourceArtifact;
        this.targetArtifact = targetArtifact;
        setIsGenerated(score);
    }

    private TraceApproval getDefaultApprovalStatus(TraceType traceType) {
        if (traceType == TraceType.MANUAL) {
            return TraceApproval.APPROVED;
        }
        return TraceApproval.UNREVIEWED;
    }

    public TraceType getTraceType() {
        return this.traceType;
    }

    public UUID getTraceLinkId() {
        return this.traceLinkId;
    }

    public void setTraceLinkId(UUID traceLinkId) {
        this.traceLinkId = traceLinkId;
    }

    private void setIsManual() {
        this.approvalStatus = TraceApproval.APPROVED;
        this.traceType = TraceType.MANUAL;
        this.score = 1;
    }

    private void setIsGenerated(double score) {
        this.approvalStatus = TraceApproval.UNREVIEWED;
        this.traceType = TraceType.GENERATED;
        this.score = score;
    }

    public String getSourceName() {
        return this.sourceArtifact.getName();
    }

    public String getTargetName() {
        return this.targetArtifact.getName();
    }

    public ArtifactType getSourceType() {
        return this.sourceArtifact.getType();
    }

    public ArtifactType getTargetType() {
        return this.targetArtifact.getType();
    }

    public double getScore() {
        return this.score;
    }

    public TraceApproval getApprovalStatus() {
        return this.approvalStatus;
    }

    public void setApprovalStatus(TraceApproval approvalStatus) {
        this.approvalStatus = approvalStatus;
    }

    public String toString() {
        JSONObject json = new JSONObject();
        json.put("link", String.format("%s -> %s", sourceArtifact, targetArtifact));
        json.put("approved", getApprovalStatus());
        return json + "\n";
    }

    public boolean isSourceName(String sourceName) {
        return this.sourceArtifact.getName().equals(sourceName);
    }

    public boolean isTargetName(String targetName) {
        return this.targetArtifact.getName().equals(targetName);
    }

    public Artifact getSourceArtifact() {
        return this.sourceArtifact;
    }

    public void setSourceArtifact(Artifact sourceArtifact) {
        this.sourceArtifact = sourceArtifact;
    }

    public Artifact getTargetArtifact() {
        return this.targetArtifact;
    }

    public void setTargetArtifact(Artifact targetArtifact) {
        this.targetArtifact = targetArtifact;
    }
}
