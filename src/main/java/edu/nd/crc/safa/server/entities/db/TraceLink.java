package edu.nd.crc.safa.server.entities.db;

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
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;

import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;
import org.json.JSONObject;

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

    public TraceLink() {
    }

    public TraceLink(TraceAppEntity traceLink) {
        String traceLinkId = traceLink.getTraceLinkId();
        if (traceLinkId != null && !traceLinkId.equals("")) {
            this.traceLinkId = UUID.fromString(traceLink.getTraceLinkId());
        }
    }

    public TraceLink(Artifact sourceArtifact,
                     Artifact targetArtifact) {
        this.sourceArtifact = sourceArtifact;
        this.targetArtifact = targetArtifact;
    }

    public UUID getTraceLinkId() {
        return this.traceLinkId;
    }

    public void setTraceLinkId(UUID traceLinkId) {
        this.traceLinkId = traceLinkId;
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

    public String toString() {
        JSONObject json = new JSONObject();
        json.put("link", String.format("%s -> %s", sourceArtifact, targetArtifact));
        return json + "\n";
    }

    public boolean isSourceName(String sourceName) {
        return this.sourceArtifact.getBaseEntityId().equals(sourceName);
    }

    public boolean isTargetName(String targetName) {
        return this.targetArtifact.getBaseEntityId().equals(targetName);
    }

    public Artifact getSourceArtifact() {
        return this.sourceArtifact;
    }

    public void setSourceArtifact(Artifact sourceArtifact) {
        this.sourceArtifact = sourceArtifact;
    }

    public Artifact getTargetArtifact() {
        return this.targetArtifact;
    }

    public void setTargetArtifact(Artifact targetArtifact) {
        this.targetArtifact = targetArtifact;
    }

    @Override
    public String getBaseEntityId() {
        return this.getTraceName();
    }

    public boolean equals(TraceLink other) {
        return this.sourceArtifact.getArtifactId().equals(other.sourceArtifact.getArtifactId())
            && this.targetArtifact.getArtifactId().equals(other.targetArtifact.getArtifactId());
    }

    public String getTraceName() {
        return this.getSourceName() + "-" + this.getTargetName();
    }
}
