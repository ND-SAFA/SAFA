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

import edu.nd.crc.safa.output.error.ServerError;

import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;

/**
 * Responsible for marking each trace link in each project.
 */
@Entity
@Table(name = "trace_links")
public class TraceLink implements Serializable {

    @Id
    @Column(name = "trace_link_id")
    @GeneratedValue
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
        if (!sourceArtifact.project.equals(targetArtifact.project)) {
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
}
