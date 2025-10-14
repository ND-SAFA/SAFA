package edu.nd.crc.safa.features.documents.entities.db;

import java.io.Serializable;
import java.util.UUID;

import edu.nd.crc.safa.config.AppConstraints;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import jakarta.persistence.UniqueConstraint;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

/**
 * Responsible for storing the connection between artifacts and a
 * document.
 */
@Entity
@Table(name = "document_artifact",
    uniqueConstraints = {
        @UniqueConstraint(
            columnNames = {
                "document_id",
                "artifact_id"
            }, name = AppConstraints.UNIQUE_ARTIFACT_PER_DOCUMENT)
    })
public class DocumentArtifact implements Serializable {

    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column(name = "document_artifact_id")
    private UUID documentArtifactId;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "version_id",
        nullable = false
    )
    private ProjectVersion projectVersion;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "document_id",
        nullable = false
    )
    private Document document;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "artifact_id",
        nullable = false)
    private Artifact artifact;

    public DocumentArtifact() {
    }

    public DocumentArtifact(ProjectVersion projectVersion,
                            Document document,
                            Artifact artifact) {
        this.projectVersion = projectVersion;
        this.document = document;
        this.artifact = artifact;
    }

    public ProjectVersion getProjectVersion() {
        return projectVersion;
    }

    public void setProjectVersion(ProjectVersion projectVersion) {
        this.projectVersion = projectVersion;
    }

    public Document getDocument() {
        return document;
    }

    public void setDocument(Document document) {
        this.document = document;
    }

    public UUID getDocumentArtifactId() {
        return documentArtifactId;
    }

    public void setDocumentArtifactId(UUID documentArtifactId) {
        this.documentArtifactId = documentArtifactId;
    }

    public Artifact getArtifact() {
        return artifact;
    }

    public void setArtifact(Artifact artifact) {
        this.artifact = artifact;
    }
}
