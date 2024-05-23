package edu.nd.crc.safa.features.artifacts.entities.db;

import java.io.Serializable;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.config.AppConstraints;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.common.IVersionEntity;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import com.fasterxml.jackson.databind.JsonNode;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.Lob;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import jakarta.persistence.Transient;
import jakarta.persistence.UniqueConstraint;
import lombok.Data;
import lombok.Setter;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

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
    @Setter
    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column
    private UUID entityVersionId;

    @Column(name = "modification_type", nullable = false)
    @JdbcTypeCode(SqlTypes.INTEGER)
    @Enumerated(EnumType.ORDINAL)
    private ModificationType modificationType;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "artifact_id", nullable = false)
    private Artifact artifact;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "version_id",
        nullable = false
    )
    private ProjectVersion projectVersion;

    @Column(name = "summary", nullable = false)
    private String summary;

    @Lob
    @Column(name = "content",
        nullable = false,
        columnDefinition = "mediumtext")
    private String content;

    @Transient
    private Map<String, JsonNode> customAttributeValues;

    @Transient
    private List<UUID> documentIds;

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

    public ArtifactType getType() {
        return this.artifact.getType();
    }

    /**
     * Adds a custom attribute value to this ArtifactVersion object. This does NOT associate this
     * custom attribute value with this artifact version in the database. It is merely a convenience so
     * that all attribute values associated with this artifact version can be stored in a single
     * object temporarily while this object is in flight.
     *
     * @param keyname The key for the attribute.
     * @param value   The value of the attribute as a json node.
     */
    public void addCustomAttributeValue(String keyname, JsonNode value) {
        customAttributeValues.put(keyname, value);
    }

    public boolean hasSameContent(IVersionEntity entityVersion) {
        if (entityVersion instanceof ArtifactVersion artifactVersion) {
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

    private boolean hasSameContent(String name, String summary, String content, Map<String, JsonNode> attributes) {
        return this.getName().equals(name)
            && this.summary.equals(summary)
            && this.content.equals(content)
            && this.customAttributeValues.equals(attributes);
    }
}
