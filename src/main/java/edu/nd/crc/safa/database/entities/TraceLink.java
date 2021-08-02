package edu.nd.crc.safa.database.entities;

import java.io.Serializable;
import java.util.UUID;

import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

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

    @ManyToOne(cascade = CascadeType.REMOVE)
    @JoinColumn(
        name = "artifact_id",
        nullable = false
    )
    Artifact sourceArtifact;


    @ManyToOne(cascade = CascadeType.REMOVE)
    @JoinColumn(
        name = "artifact_id",
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
                     Artifact targetArtifact) {
        this();
        this.sourceArtifact = sourceArtifact;
        this.targetArtifact = targetArtifact;
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
