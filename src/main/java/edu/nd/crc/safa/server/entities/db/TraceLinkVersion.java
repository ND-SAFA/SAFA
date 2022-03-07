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

import edu.nd.crc.safa.config.AppConstraints;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;

import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;
import org.json.JSONObject;

/**
 * Responsible for marking each trace link in each project.
 */
@Entity
@Table(name = "trace_link_version",
    uniqueConstraints = {
        @UniqueConstraint(columnNames = {
            "version_id", "trace_link_id"
        }, name = AppConstraints.SINGLE_TRACE_VERSION_PER_PROJECT_VERSION)
    }
)
public class TraceLinkVersion implements Serializable, IVersionEntity<TraceAppEntity> {

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "trace_link_version_id")
    UUID traceLinkVersionId;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "version_id",
        nullable = false
    )
    ProjectVersion projectVersion;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "trace_link_id",
        nullable = false
    )
    TraceLink traceLink;

    @Column(name = "modification_type", nullable = false)
    @Enumerated(EnumType.ORDINAL)
    ModificationType modificationType;

    @Column(name = "trace_type", nullable = false)
    @Enumerated(EnumType.ORDINAL)
    TraceType traceType;

    @Column(name = "approval_status")
    TraceApproval approvalStatus;

    @Column(name = "score")
    double score;

    public TraceLinkVersion() {
        this.traceType = TraceType.GENERATED;
        this.approvalStatus = TraceApproval.UNREVIEWED;
        this.score = 0;
    }

    public static TraceLinkVersion createGeneratedLinkWithVersionAndModification(ProjectVersion projectVersion,
                                                                                 ModificationType modificationType,
                                                                                 TraceLink traceLink,
                                                                                 double score) {
        TraceLinkVersion traceLinkVersion = new TraceLinkVersion();
        traceLinkVersion.projectVersion = projectVersion;
        traceLinkVersion.modificationType = modificationType;
        traceLinkVersion.traceLink = traceLink;
        traceLinkVersion.score = score;
        traceLinkVersion.traceType = TraceType.GENERATED;
        traceLinkVersion.approvalStatus = TraceApproval.UNREVIEWED;

        return traceLinkVersion;
    }

    public static TraceLinkVersion createLinkWithVersionAndModificationAndTraceAppEntity(
        ProjectVersion projectVersion,
        ModificationType modificationType,
        TraceLink traceLink,
        TraceAppEntity traceAppEntity) {
        TraceLinkVersion traceLinkVersion = new TraceLinkVersion();
        traceLinkVersion.traceType = traceAppEntity.traceType == null ? TraceType.MANUAL : traceAppEntity.traceType;
        traceLinkVersion.approvalStatus = traceAppEntity.approvalStatus == null
            ? getDefaultApprovalStatus(traceLinkVersion.traceType) :
            traceAppEntity.approvalStatus;
        traceLinkVersion.score = traceAppEntity.score == 0 ? traceLinkVersion.score : traceAppEntity.score;
        traceLinkVersion.projectVersion = projectVersion;
        traceLinkVersion.modificationType = modificationType;
        traceLinkVersion.traceLink = traceLink;

        return traceLinkVersion;
    }

    private static TraceApproval getDefaultApprovalStatus(TraceType traceType) {
        if (traceType == TraceType.MANUAL) {
            return TraceApproval.APPROVED;
        }
        return TraceApproval.UNREVIEWED;
    }

    public TraceLinkVersion withProjectVersion(ProjectVersion projectVersion) {
        setProjectVersion(projectVersion);
        return this;
    }

    public TraceLinkVersion withModificationType(ModificationType modificationType) {
        setModificationType(modificationType);
        return this;
    }

    public TraceLinkVersion withTraceLink(TraceLink traceLink) {
        setTraceLink(traceLink);
        return this;
    }

    public TraceLinkVersion withManualTraceType() {
        setTraceType(TraceType.MANUAL);
        setApprovalStatus(TraceApproval.APPROVED);
        setScore(1);
        return this;
    }

    public UUID getTraceLinkVersionId() {
        return traceLinkVersionId;
    }

    public void setTraceLinkVersionId(UUID traceLinkVersionId) {
        this.traceLinkVersionId = traceLinkVersionId;
    }

    public TraceLink getTraceLink() {
        return traceLink;
    }

    public void setTraceLink(TraceLink traceLink) {
        this.traceLink = traceLink;
    }

    public TraceType getTraceType() {
        return this.traceType;
    }

    public void setTraceType(TraceType traceType) {
        this.traceType = traceType;
    }

    public double getScore() {
        return this.score;
    }

    public void setScore(double score) {
        this.score = score;
    }

    public TraceApproval getApprovalStatus() {
        return this.approvalStatus;
    }

    public void setApprovalStatus(TraceApproval approvalStatus) {
        this.approvalStatus = approvalStatus;
    }

    public String toString() {
        JSONObject json = new JSONObject();
        json.put("mod", this.modificationType);
        json.put("version", this.projectVersion);
        json.put("link", this.traceLink.toString());
        json.put("approved", getApprovalStatus());
        json.put("type", this.traceType);
        return json + "\n";
    }

    @Override
    public ProjectVersion getProjectVersion() {
        return this.projectVersion;
    }

    public void setProjectVersion(ProjectVersion projectVersion) {
        this.projectVersion = projectVersion;
    }

    @Override
    public ModificationType getModificationType() {
        return this.modificationType;
    }

    public void setModificationType(ModificationType modificationType) {
        this.modificationType = modificationType;
    }

    @Override
    public String getBaseEntityId() {
        return traceLink.getBaseEntityId();
    }

    @Override
    public boolean hasSameContent(IVersionEntity e) {
        if (e instanceof TraceLinkVersion) {
            TraceLinkVersion other = (TraceLinkVersion) e;
            return hasSameContent(
                other.traceLink.sourceArtifact.getName(),
                other.traceLink.targetArtifact.getName(),
                other.traceType,
                other.approvalStatus,
                other.score
            );
        }
        return false;
    }

    @Override
    public boolean hasSameContent(TraceAppEntity other) {
        return hasSameContent(
            other.sourceName,
            other.targetName,
            other.traceType,
            other.approvalStatus,
            other.score
        );
    }

    private boolean hasSameContent(String sourceName,
                                   String targetName,
                                   TraceType traceType,
                                   TraceApproval traceApproval,
                                   double score) {
        return this.traceLink.sourceArtifact.getName().equals(sourceName)
            && this.traceLink.targetArtifact.getName().equals(targetName)
            && this.traceType == traceType
            && this.approvalStatus == traceApproval
            && areEqualWithDelta(this.score, score, 0.001);
    }

    private boolean areEqualWithDelta(double a, double b, double delta) {
        return Math.abs(a - b) < delta;
    }
}
