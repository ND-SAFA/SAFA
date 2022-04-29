package edu.nd.crc.safa.server.entities.db;

import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.OneToOne;
import javax.persistence.Table;

import edu.nd.crc.safa.server.entities.app.project.SafetyCaseType;

import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

/**
 * Persists the information needed to represent safety-case specific
 * artifacts.
 */
@Entity
@Table(name = "safety_case_artifact")
public class SafetyCaseArtifact implements IArtifact {

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "safety_case_artifact_id")
    UUID safetyCaseArtifactId;
    @OneToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "artifact_id", nullable = false, unique = true)
    Artifact artifact;
    @Column(name = "safety_case_type")
    SafetyCaseType safetyCaseType;

    public SafetyCaseArtifact() {
    }

    public SafetyCaseArtifact(Artifact artifact, SafetyCaseType safetyCaseType) {
        this.artifact = artifact;
        this.safetyCaseType = safetyCaseType;
    }

    public Artifact getArtifact() {
        return artifact;
    }

    public void setArtifact(Artifact artifact) {
        this.artifact = artifact;
    }

    public SafetyCaseType getSafetyCaseType() {
        return safetyCaseType;
    }

    public void setSafetyCaseType(SafetyCaseType safetyCaseType) {
        this.safetyCaseType = safetyCaseType;
    }

    @Override
    public String getName() {
        return this.artifact.getName();
    }
}
