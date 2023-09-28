package edu.nd.crc.safa.features.traces.entities.db;

import java.io.Serializable;
import java.util.UUID;

import edu.nd.crc.safa.config.AppConstraints;
import edu.nd.crc.safa.features.common.IVersionEntity;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.Lob;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import jakarta.persistence.UniqueConstraint;
import lombok.Data;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

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
@Data
public class TraceLinkVersion implements Serializable, IVersionEntity<TraceAppEntity> {

    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column(name = "trace_link_version_id")
    private UUID traceLinkVersionId;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "version_id",
        nullable = false
    )
    private ProjectVersion projectVersion;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "trace_link_id",
        nullable = false
    )
    private TraceLink traceLink;

    @Column(name = "modification_type", nullable = false)
    @JdbcTypeCode(SqlTypes.INTEGER)
    @Enumerated(EnumType.ORDINAL)
    private ModificationType modificationType;

    @Column(name = "trace_type", nullable = false)
    @JdbcTypeCode(SqlTypes.INTEGER)
    @Enumerated(EnumType.ORDINAL)
    private TraceType traceType;
    @JdbcTypeCode(SqlTypes.INTEGER)
    @Column(name = "approval_status")
    private ApprovalStatus approvalStatus;

    @Column(name = "score")
    private double score;

    @Column(name = "is_visible")
    private boolean isVisible = true;

    @Lob
    @Column(columnDefinition = "text")
    private String explanation;

    public TraceLinkVersion() {
        this.traceType = TraceType.GENERATED;
        this.approvalStatus = ApprovalStatus.UNREVIEWED;
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
        traceLinkVersion.approvalStatus = ApprovalStatus.UNREVIEWED;

        return traceLinkVersion;
    }

    public static TraceLinkVersion createLinkWithVersionAndModificationAndTraceAppEntity(
        ProjectVersion projectVersion,
        ModificationType modificationType,
        TraceLink traceLink,
        TraceAppEntity traceAppEntity) {
        TraceLinkVersion traceLinkVersion = new TraceLinkVersion();
        traceLinkVersion.traceType = traceAppEntity.getTraceType() == null
            ? TraceType.MANUAL : traceAppEntity.getTraceType();
        traceLinkVersion.approvalStatus = traceAppEntity.getApprovalStatus() == null
            ? getDefaultApprovalStatus(traceLinkVersion.traceType) :
            traceAppEntity.getApprovalStatus();
        traceLinkVersion.isVisible = traceAppEntity.isVisible();
        traceLinkVersion.score = traceAppEntity.getScore() == 0 ? traceLinkVersion.score : traceAppEntity.getScore();
        traceLinkVersion.projectVersion = projectVersion;
        traceLinkVersion.modificationType = modificationType;
        traceLinkVersion.traceLink = traceLink;
        traceLinkVersion.explanation = traceAppEntity.getExplanation();
        return traceLinkVersion;
    }

    private static ApprovalStatus getDefaultApprovalStatus(TraceType traceType) {
        if (traceType == TraceType.MANUAL) {
            return ApprovalStatus.APPROVED;
        }
        return ApprovalStatus.UNREVIEWED;
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
        setApprovalStatus(ApprovalStatus.APPROVED);
        setScore(1);
        return this;
    }

    public TraceLinkVersion withApprovalStatus(ApprovalStatus approvalStatus) {
        this.setApprovalStatus(approvalStatus);
        return this;
    }

    public TraceLinkVersion withScore(double score) {
        this.setScore(score);
        return this;
    }

    public TraceLinkVersion withVisibility(boolean isVisible) {
        this.setVisible(isVisible);
        return this;
    }

    @Override
    public UUID getBaseEntityId() {
        return traceLink.getBaseEntityId();
    }

    @Override
    public UUID getVersionEntityId() {
        return this.traceLinkVersionId;
    }

    @Override
    public void setVersionEntityId(UUID versionEntityId) {
        this.traceLinkVersionId = versionEntityId;
    }

    @Override
    public boolean hasSameContent(IVersionEntity e) {
        if (e instanceof TraceLinkVersion) {
            TraceLinkVersion other = (TraceLinkVersion) e;
            return hasSameContent(
                other.traceLink.getSourceArtifact().getName(),
                other.traceLink.getTargetArtifact().getName(),
                other.traceType,
                other.approvalStatus,
                other.score,
                other.isVisible
            );
        }
        return false;
    }

    @Override
    public boolean hasSameContent(TraceAppEntity other) {
        return hasSameContent(
            other.getSourceName(),
            other.getTargetName(),
            other.getTraceType(),
            other.getApprovalStatus(),
            other.getScore(),
            other.isVisible()
        );
    }

    private boolean hasSameContent(String sourceName,
                                   String targetName,
                                   TraceType traceType,
                                   ApprovalStatus approvalStatus,
                                   double score,
                                   boolean isVisible) {
        return this.traceLink.getSourceArtifact().getName().equals(sourceName)
            && this.traceLink.getTargetArtifact().getName().equals(targetName)
            && this.traceType == traceType
            && this.approvalStatus == approvalStatus
            && areEqualWithDelta(this.score, score, 0.001)
            && this.isVisible == isVisible;
    }

    private boolean areEqualWithDelta(double a, double b, double delta) {
        return Math.abs(a - b) < delta;
    }
}
