package edu.nd.crc.safa.entities;

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
    Artifact sourceId;

    @Id
    @ManyToOne(cascade = CascadeType.REMOVE)
    @JoinColumn(
        name = "artifact_id",
        nullable = false
    )
    Artifact targetId;

    @ManyToOne(cascade = CascadeType.REMOVE)
    @JoinColumn(
        name = "trace_type_id",
        nullable = false
    )
    TraceType type;

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
}
