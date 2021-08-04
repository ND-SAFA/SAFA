package edu.nd.crc.safa.entities;

import java.io.Serializable;
import java.util.UUID;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;

/**
 * Responsible for storing an artifact's different contents
 * depending on the project version.
 */
@Entity
@Table(name = "artifact_contents")
public class ArtifactBody implements Serializable {
    @Id
    @GeneratedValue
    @Column
    UUID artifactBodyId;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "artifact_id")
    Artifact artifact;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "version_id",
        nullable = false
    )
    ProjectVersion projectVersion;

    @Column(name = "summary")
    String summary;

    @Column(name = "content")
    String content;

    public ArtifactBody() {
    }

    public ArtifactBody(Artifact artifact,
                        ProjectVersion projectVersion,
                        String summary,
                        String content) {
        this.artifact = artifact;
        this.projectVersion = projectVersion;
        this.summary = summary;
        this.content = content;
    }

    public String getName() {
        return this.artifact.getName();
    }

    public String getTypeName() {
        return this.artifact.getType().getName();
    }

    public String getContent() {
        return this.content;
    }

    public String getSummary() {
        return this.summary;
    }
}
