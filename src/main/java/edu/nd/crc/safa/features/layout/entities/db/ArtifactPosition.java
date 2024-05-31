package edu.nd.crc.safa.features.layout.entities.db;

import java.util.UUID;

import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.Data;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

/**
 * Stored position of artifact in tree for at a specific version.
 */
@Entity
@Table
@Data
public class ArtifactPosition {
    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column(name = "id")
    private UUID id;
    /**
     * The version in which artifact with this position exist in.
     */
    @Column(nullable = false)
    @JdbcTypeCode(SqlTypes.VARCHAR)
    private UUID artifactId;
    /**
     * The version in which artifact with this position exist in.
     */
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "version_id", nullable = false)
    private ProjectVersion projectVersion;
    /**
     * The document this layout is setting this artifact at.
     */
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "documentId")
    private Document document;
    /**
     * How many pixels right from the top left corner of the graph.
     */
    @Column(nullable = false)
    private double x;
    /**
     * How many pixels down from the top left corner of the graph.
     */
    @Column(nullable = false)
    private double y;
}
