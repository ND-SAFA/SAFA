package edu.nd.crc.safa.database.entities;

import java.io.Serializable;

import javax.persistence.CascadeType;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.JoinColumns;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

@Entity
@Table(name = "trace_links")
public class TraceLink implements Serializable {
    @Id
    @ManyToOne(cascade = CascadeType.REMOVE)
    @JoinColumn(
        name = "artifact_id",
        nullable = false
    )
    Artifact sourceArtifact;

    @Id
    @ManyToOne(cascade = CascadeType.REMOVE)
    @JoinColumn(
        name = "artifact_id",
        nullable = false
    )
    Artifact targetArtifact;

    @ManyToOne(cascade = CascadeType.REMOVE)
    @JoinColumn(
        name = "trace_type_id",
        nullable = false
    )
    TraceType traceType;

    @ManyToOne(cascade = CascadeType.REMOVE)
    @JoinColumns({
        @JoinColumn(
            name = "project_id",
            nullable = false
        ),
        @JoinColumn(
            name = "version_id",
            nullable = false
        )
    })
    ProjectVersion projectVersion;

    public TraceLink() {
    }

    public TraceLink(Artifact sourceArtifact,
                     Artifact targetArtifact,
                     TraceType traceType) {
        this.sourceArtifact = sourceArtifact;
        this.targetArtifact = targetArtifact;
        this.traceType = traceType;
    }
}
