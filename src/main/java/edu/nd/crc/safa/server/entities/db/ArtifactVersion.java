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
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;

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
        }, name = AppConstraints.UNIQUE_ARTIFACT_BODY_PER_VERSION)
    }
)
public class ArtifactVersion implements Serializable, IVersionEntity<ArtifactAppEntity> {
    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column
    UUID entityVersionId;

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

    public ArtifactVersion() {
        this.summary = "";
        this.content = "";
    }

    public ArtifactVersion(ProjectVersion projectVersion,
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

    public ArtifactVersion(ProjectVersion projectVersion,
                           Artifact artifact,
                           String summary,
                           String content) {
        this(projectVersion, ModificationType.ADDED, artifact, summary, content);
    }

    public UUID getEntityVersionId() {
        return this.entityVersionId;
    }

    public void setEntityVersionId(UUID artifactBodyId) {
        this.entityVersionId = artifactBodyId;
    }

    @Override
    public String getBaseEntityId() {
        return this.artifact.getBaseEntityId();
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

    public void setContent(String content) {
        this.content = content;
    }

    public String getSummary() {
        return this.summary;
    }

    public void setSummary(String summary) {
        this.summary = summary;
    }

    public Artifact getArtifact() {
        return this.artifact;
    }

    public void setArtifact(Artifact artifact) {
        this.artifact = artifact;
    }

    public ModificationType getModificationType() {
        return this.modificationType;
    }

    public void setModificationType(ModificationType modificationType) {
        this.modificationType = modificationType;
    }

    public ProjectVersion getProjectVersion() {
        return this.projectVersion;
    }

    public void setProjectVersion(ProjectVersion projectVersion) {
        this.projectVersion = projectVersion;
    }

    public boolean hasSameId(ArtifactVersion other) {
        return this.entityVersionId.equals(other.entityVersionId);
    }

    public String toString() {
        JSONObject json = new JSONObject();
        json.put("artifact", artifact);
        json.put("summary", this.summary);
        json.put("body", this.content);
        json.put("modificationType", modificationType);
        return json.toString();
    }

    public boolean hasSameContent(IVersionEntity entityVersion) {
        if (entityVersion instanceof ArtifactVersion) {
            ArtifactVersion artifactVersion = (ArtifactVersion) entityVersion;
            return hasSameContent(artifactVersion.getName(),
                artifactVersion.getSummary(),
                artifactVersion.getContent());
        }
        return false;
    }

    public boolean hasSameContent(ArtifactAppEntity a) {
        return hasSameContent(a.name, a.summary, a.body);
    }

    private boolean hasSameContent(String name, String summary, String content) {
        return this.getName().equals(name)
            && this.summary.equals(summary)
            && this.content.equals(content);
    }
}
