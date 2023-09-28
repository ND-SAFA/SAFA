package edu.nd.crc.safa.features.artifacts.entities.db;

import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.SafetyCaseType;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

/**
 * Persists the information needed to represent safety-case specific
 * artifacts.
 */
@Entity
@Table(name = "safety_case_artifact")
@Data
@NoArgsConstructor
public class SafetyCaseArtifact implements IArtifact {

    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column(name = "safety_case_artifact_id")
    private UUID safetyCaseArtifactId;
    @OneToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "artifact_id", nullable = false, unique = true)
    private Artifact artifact;
    @JdbcTypeCode(SqlTypes.INTEGER)
    @Column(name = "safety_case_type")
    private SafetyCaseType safetyCaseType;

    public SafetyCaseArtifact(Artifact artifact, SafetyCaseType safetyCaseType) {
        this.artifact = artifact;
        this.safetyCaseType = safetyCaseType;
    }

    @Override
    public String getName() {
        return this.artifact.getName();
    }
}
