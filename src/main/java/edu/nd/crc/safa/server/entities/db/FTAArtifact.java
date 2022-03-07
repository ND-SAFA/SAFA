package edu.nd.crc.safa.server.entities.db;

import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.OneToOne;
import javax.persistence.Table;

import edu.nd.crc.safa.server.entities.app.FTANodeType;

import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

/**
 * The persistent data for an FTA artifact.
 */
@Entity
@Table(name = "fta_artifact")
public class FTAArtifact {
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
    @JoinColumn(name = "artifact_id", nullable = false)
    Artifact artifact;
    /**
     * The artifact type of the parent node.
     */
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(nullable = false)
    ArtifactType parentType;

    /**
     * For FTA nodes, the logic type of the artifact.
     */
    @Column(name = "logic_type")
    FTANodeType logicType;

    public FTAArtifact() {
    }

    public FTAArtifact(Artifact artifact, ArtifactType parentType, FTANodeType ftaNodeType) {
        this.artifact = artifact;
        this.parentType = parentType;
        this.logicType = ftaNodeType;
    }
}
