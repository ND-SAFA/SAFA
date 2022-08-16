package edu.nd.crc.safa.features.traces.entities.db;

import java.io.Serializable;
import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;
import javax.persistence.UniqueConstraint;

import edu.nd.crc.safa.config.AppConstraints;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.types.ArtifactType;
import edu.nd.crc.safa.features.common.IBaseEntity;

import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

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
    @Type(type = "uuid-char")
    @Column(name = "trace_link_id")
    UUID traceLinkId;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "source_artifact_id",
        referencedColumnName = "artifact_id",
        nullable = false
    )
    Artifact sourceArtifact;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "target_artifact_id",
        referencedColumnName = "artifact_id",
        nullable = false
    )
    Artifact targetArtifact;

    public TraceLink(Artifact sourceArtifact,
                     Artifact targetArtifact) {
        this.sourceArtifact = sourceArtifact;
        this.targetArtifact = targetArtifact;
    }

    public String getSourceName() {
        return this.sourceArtifact.getBaseEntityId();
    }

    public String getTargetName() {
        return this.targetArtifact.getBaseEntityId();
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
    public String getBaseEntityId() {
        return this.getTraceLinkId().toString();
    }
}
