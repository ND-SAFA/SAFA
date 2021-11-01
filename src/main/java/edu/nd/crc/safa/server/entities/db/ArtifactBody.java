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

import edu.nd.crc.safa.config.ProjectVariables;

import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;
import org.json.JSONObject;

/**
 * Responsible for storing an artifact's different contents
 * depending on the project version.
 */
@Entity
@Table(name = "artifact_body",
    uniqueConstraints = {
        @UniqueConstraint(columnNames = {
            "artifact_id", "version_id"
        }, name = "UNIQUE_ARTIFACT_BODY_PER_VERSION")
    }
)
public class ArtifactBody implements Serializable {
    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column
    UUID artifactBodyId;

    @Column(name = "modification_type")
    @Enumerated(EnumType.ORDINAL)
    ModificationType modificationType;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "artifact_id", nullable = false)
    Artifact artifact;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "version_id",
        nullable = false
    )
    ProjectVersion projectVersion;

    @Column(name = "summary", nullable = false)
    String summary;

    @Column(name = "content", length = ProjectVariables.ARTIFACT_CONTENT_LENGTH, nullable = false)
    String content;

    public ArtifactBody() {
        this.summary = "";
        this.content = "";
    }

    public ArtifactBody(ProjectVersion projectVersion,
                        ModificationType modificationType,
                        Artifact artifact,
                        String summary,
                        String content) {
        this.artifact = artifact;
        this.modificationType = modificationType;
        this.projectVersion = projectVersion;
        this.summary = summary;
        this.content = content;
    }

    public ArtifactBody(ProjectVersion projectVersion,
                        Artifact artifact,
                        String summary,
                        String content) {
        this(projectVersion, ModificationType.ADDED, artifact, summary, content);
    }

    public UUID getArtifactBodyId() {
        return this.artifactBodyId;
    }

    public void setArtifactBodyId(UUID artifactBodyId) {
        this.artifactBodyId = artifactBodyId;
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

    public Artifact getArtifact() {
        return this.artifact;
    }

    public ModificationType getModificationType() {
        return this.modificationType;
    }

    public ProjectVersion getProjectVersion() {
        return this.projectVersion;
    }

    public boolean hasSameId(ArtifactBody other) {
        return this.artifactBodyId.equals(other.artifactBodyId);
    }

    public String toString() {
        JSONObject json = new JSONObject();
        json.put("artifact", artifact);
        json.put("summary", this.summary);
        json.put("body", this.content);
        json.put("modificationType", modificationType);
        return json.toString();
    }
}
