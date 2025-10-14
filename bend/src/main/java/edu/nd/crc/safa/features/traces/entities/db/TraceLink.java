package edu.nd.crc.safa.features.traces.entities.db;

import java.io.Serializable;
import java.util.UUID;

import edu.nd.crc.safa.config.AppConstraints;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.common.IBaseEntity;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import jakarta.persistence.UniqueConstraint;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

/**
 * Identifies a series of versioned trace links between a source
 * and target artifacts.
 */
@Entity
@Table(name = "trace_link",
    uniqueConstraints = {
        @UniqueConstraint(columnNames = {
            "source_artifact_id", "target_artifact_id"
        }, name = AppConstraints.SINGLE_TRACE_BETWEEN_SOURCE_AND_TARGET)
    }
)
@Data
@NoArgsConstructor
public class TraceLink implements Serializable, IBaseEntity {

    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column(name = "trace_link_id")
    private UUID traceLinkId;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "source_artifact_id",
        referencedColumnName = "artifact_id",
        nullable = false
    )
    private Artifact sourceArtifact;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "target_artifact_id",
        referencedColumnName = "artifact_id",
        nullable = false
    )
    private Artifact targetArtifact;

    public TraceLink(Artifact sourceArtifact,
                     Artifact targetArtifact) {
        this.sourceArtifact = sourceArtifact;
        this.targetArtifact = targetArtifact;
    }

    public String getSourceName() {
        return this.sourceArtifact.getName();
    }

    public String getTargetName() {
        return this.targetArtifact.getName();
    }

    public ArtifactType getSourceType() {
        return this.sourceArtifact.getType();
    }

    public ArtifactType getTargetType() {
        return this.targetArtifact.getType();
    }

    public boolean isSourceName(String sourceName) {
        return this.sourceArtifact.getName().equals(sourceName);
    }

    public boolean isTargetName(String targetName) {
        return this.targetArtifact.getName().equals(targetName);
    }

    @Override
    public UUID getBaseEntityId() {
        return this.getTraceLinkId();
    }
}
