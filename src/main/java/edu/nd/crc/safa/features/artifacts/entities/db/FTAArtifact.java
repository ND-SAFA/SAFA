package edu.nd.crc.safa.features.artifacts.entities.db;

import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.FTAType;

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
 * The persistent data for an FTA artifact.
 */
@Entity
@Table(name = "fta_artifact")
@NoArgsConstructor
@Data
public class FTAArtifact implements IArtifact {
    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column(name = "fta_artifact_id")
    private UUID ftaArtifactId;
    /**
     * The associated base artifact.
     */
    @OneToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "artifact_id", nullable = false, unique = true)
    private Artifact artifact;
    /**
     * For FTA nodes, the logic type of the artifact (e.g. AND / OR)
     */
    @JdbcTypeCode(SqlTypes.INTEGER)
    @Column(name = "logic_type")
    private FTAType logicType;

    public FTAArtifact(Artifact artifact, FTAType ftaType) {
        this.artifact = artifact;
        this.logicType = ftaType;
    }

    public String getName() {
        return this.artifact.getName();
    }
}
