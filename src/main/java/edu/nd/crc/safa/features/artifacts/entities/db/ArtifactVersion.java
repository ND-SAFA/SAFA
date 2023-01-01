package edu.nd.crc.safa.features.artifacts.entities.db;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.Lob;
import javax.persistence.ManyToOne;
import javax.persistence.Table;
import javax.persistence.Transient;
import javax.persistence.UniqueConstraint;

import edu.nd.crc.safa.config.AppConstraints;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.common.IVersionEntity;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.Data;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

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
@Data
public class ArtifactVersion implements Serializable, IVersionEntity<ArtifactAppEntity> {
    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column
    UUID entityVersionId;

    @Column(name = "modification_type", nullable = false)
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

    @Lob
    @Column(name = "content",
        nullable = false,
        columnDefinition = "mediumtext")
    String content;

    @Transient
    private Map<String, String> customAttributeValues;

    public ArtifactVersion() {
        this.summary = "";
        this.content = "";
        this.customAttributeValues = new HashMap<>();
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
        this.customAttributeValues = new HashMap<>();
    }

    public ArtifactVersion(ProjectVersion projectVersion,
                           Artifact artifact,
                           String summary,
                           String content) {
        this(projectVersion, ModificationType.ADDED, artifact, summary, content);
    }

    @Override
    public UUID getVersionEntityId() {
        return this.entityVersionId;
    }

    public void setVersionEntityId(UUID versionEntityId) {
        this.setEntityVersionId(versionEntityId);
    }

    public void setEntityVersionId(UUID artifactBodyId) {
        this.entityVersionId = artifactBodyId;
    }

    @Override
    public UUID getBaseEntityId() {
        return this.artifact.getBaseEntityId();
    }

    public String getName() {
        return this.artifact.getName();
    }

    public String getTypeName() {
        return this.artifact.getType().getName();
    }

    public void addCustomAttributeValue(String keyname, String value) {
        customAttributeValues.put(keyname, value);
    }

    public boolean hasSameContent(IVersionEntity entityVersion) {
        if (entityVersion instanceof ArtifactVersion) {
            ArtifactVersion artifactVersion = (ArtifactVersion) entityVersion;
            return hasSameContent(artifactVersion.getName(),
                artifactVersion.getSummary(),
                artifactVersion.getContent(),
                artifactVersion.getCustomAttributeValues());
        }
        return false;
    }

    public boolean hasSameContent(ArtifactAppEntity a) {
        return hasSameContent(a.getName(), a.getSummary(), a.getBody(), a.getAttributes());
    }

    private boolean hasSameContent(String name, String summary, String content, Map<String, String> attributes) {
        return this.getName().equals(name)
            && this.summary.equals(summary)
            && this.content.equals(content)
            && this.customAttributeValues.equals(attributes);
    }
}
