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

    @Column(name = "approved")
    TraceApproval approvalStatus;

    @Column(name = "score")
    double score;

    public TraceLinkVersion() {
        this.traceType = TraceType.GENERATED;
        this.approvalStatus = TraceApproval.UNREVIEWED;
        this.score = 0;
    }

    public TraceLinkVersion(ProjectVersion projectVersion,
                            ModificationType modificationType,
                            TraceLink traceLink) {
        this();
        this.projectVersion = projectVersion;
        this.modificationType = modificationType;
        this.traceLink = traceLink;
    }

    public TraceLinkVersion(ProjectVersion projectVersion,
                            ModificationType modificationType,
                            TraceLink traceLink,
                            double score) {
        this();
        this.projectVersion = projectVersion;
        this.modificationType = modificationType;
        this.traceLink = traceLink;
        this.score = score;
        this.traceType = TraceType.GENERATED;
    }

    public TraceLinkVersion(TraceAppEntity traceAppEntity) {
        this();
        System.out.println("Creating version from:" + traceAppEntity);
        this.traceType = traceAppEntity.traceType == null ? TraceType.MANUAL : traceAppEntity.traceType;
        this.approvalStatus = traceAppEntity.approvalStatus == null ? getDefaultApprovalStatus(this.traceType) :
            traceAppEntity.approvalStatus;
        this.score = traceAppEntity.score == 0 ? this.score : traceAppEntity.score;
        //TODO:Remove when tests pas
//        String traceLinkId = traceLink.getTraceLinkId();
//        if (traceLinkId != null && !traceLinkId.equals("")) {
//            this.traceLinkId = UUID.fromString(traceLink.getTraceLinkId());
//        }
    }

    public TraceLinkVersion(ProjectVersion projectVersion,
                            ModificationType modificationType,
                            TraceLink traceLink,
                            TraceAppEntity traceAppEntity) {
        this(traceAppEntity);
        this.projectVersion = projectVersion;
        this.modificationType = modificationType;
        this.traceLink = traceLink;
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

    private TraceApproval getDefaultApprovalStatus(TraceType traceType) {
        if (traceType == TraceType.MANUAL) {
            return TraceApproval.APPROVED;
        }
        return TraceApproval.UNREVIEWED;
    }

    public TraceType getTraceType() {
        return this.traceType;
    }

    public void setTraceType(TraceType traceType) {
        this.traceType = traceType;
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
        json.put("version", this.projectVersion);
        json.put("link", this.traceLink.toString());
        json.put("approved", getApprovalStatus());
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
                other.traceLink.sourceArtifact.getBaseEntityId(),
                other.traceLink.targetArtifact.getBaseEntityId(),
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
            other.source,
            other.target,
            other.traceType,
            other.approvalStatus,
            other.score
        );
    }

    private boolean hasSameContent(String source,
                                   String target,
                                   TraceType traceType,
                                   TraceApproval traceApproval,
                                   double score) {
        return this.traceLink.sourceArtifact.getBaseEntityId().equals(source)
            && this.traceLink.targetArtifact.getBaseEntityId().equals(target)
            && this.traceType == traceType
            && this.approvalStatus == traceApproval
            && this.score == score;
    }
}
