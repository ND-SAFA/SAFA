package edu.nd.crc.safa.entities;

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

import edu.nd.crc.safa.responses.ServerError;

import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

/**
 * Responsible for marking each trace link in each project.
 */
@Entity
@Table(name = "trace_links")
public class TraceLink implements Serializable {

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "trace_link_id")
    UUID traceLinkId;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "project_id",
        nullable = false
    )
    Project project;

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
    boolean approved;

    @Column(name = "score")
    double score;

    public TraceLink() {
        this.approved = false;
        this.score = 0;
    }

    public TraceLink(Artifact sourceArtifact,
                     Artifact targetArtifact) throws ServerError {
        this();
        this.sourceArtifact = sourceArtifact;
        this.targetArtifact = targetArtifact;
        if (!sourceArtifact.project.getProjectId().equals(targetArtifact.project.getProjectId())) {
            throw new ServerError("Source and target artifacts exist in different projects");
        }
        this.project = sourceArtifact.project;
    }

    public TraceType getTraceType() {
        return this.traceType;
    }

    public UUID getTraceLinkId() {
        return this.traceLinkId;
    }

    public void setIsManual() {
        this.approved = true;
        this.traceType = TraceType.MANUAL;
        this.score = 1;
    }

    public void setIsGenerated(double score) {
        this.approved = false;
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

    public boolean isApproved() {
        return this.approved;
    }
}
