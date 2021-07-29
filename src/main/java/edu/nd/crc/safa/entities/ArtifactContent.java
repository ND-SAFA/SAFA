package edu.nd.crc.safa.entities;

import java.io.Serializable;

import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.ConstraintMode;
import javax.persistence.Entity;
import javax.persistence.ForeignKey;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.JoinColumns;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

@Entity
@Table(name = "artifact_contents")
public class ArtifactContent implements Serializable {
    @Id
    @ManyToOne(cascade = CascadeType.REMOVE)
    @JoinColumn(
        name = "artifact_id",
        foreignKey = @ForeignKey(name = "artifact_id", value = ConstraintMode.PROVIDER_DEFAULT),
        nullable = false
    )
    Artifact artifact;

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

    @Column(name = "summary")
    String summary;

    @Column(name = "content")
    String content;

    public ArtifactContent() {
    }

    public ArtifactContent(Artifact artifact,
                           ProjectVersion projectVersion,
                           String summary,
                           String content) {
        this.artifact = artifact;
        this.projectVersion = projectVersion;
        this.summary = summary;
        this.content = content;
    }
}
