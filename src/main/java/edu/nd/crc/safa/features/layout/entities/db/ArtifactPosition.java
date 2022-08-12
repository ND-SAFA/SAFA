package edu.nd.crc.safa.features.layout.entities.db;

import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import lombok.Data;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

/**
 * Stored position of artifact in tree for at a specific version.
 */
@Entity
@Table
@Data
public class ArtifactPosition {
    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "id")
    UUID id;
    /**
     * The version in which artifact with this position exist in.
     */
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "artifact_id", nullable = false)
    Artifact artifact;
    /**
     * The version in which artifact with this position exist in.
     */
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "version_id", nullable = false)
    ProjectVersion projectVersion;
    /**
     * The document this layout is setting this artifact at.
     */
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "documentId")
    Document document;
    /**
     * How many pixels right from the top left corner of the graph.
     */
    @Column(nullable = false)
    double x;
    /**
     * How many pixels down from the top left corner of the graph.
     */
    @Column(nullable = false)
    double y;
}
