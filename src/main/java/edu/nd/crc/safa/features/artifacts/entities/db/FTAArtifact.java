package edu.nd.crc.safa.features.artifacts.entities.db;

import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.OneToOne;
import javax.persistence.Table;

import edu.nd.crc.safa.features.artifacts.entities.FTAType;

import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

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
    @Type(type = "uuid-char")
    @Column(name = "fta_artifact_id")
    UUID ftaArtifactId;
    /**
     * The associated base artifact.
     */
    @OneToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "artifact_id", nullable = false, unique = true)
    Artifact artifact;
    /**
     * For FTA nodes, the logic type of the artifact (e.g. AND / OR)
     */
    @Column(name = "logic_type")
    FTAType logicType;

    public FTAArtifact(Artifact artifact, FTAType ftaType) {
        this.artifact = artifact;
        this.logicType = ftaType;
    }

    public String getName() {
        return this.artifact.getName();
    }
}
