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

import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

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
    @Type(type = "uuid-char")
    @Column(name = "document_artifact_id")
    UUID documentArtifactId;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "version_id",
        nullable = false
    )
    ProjectVersion projectVersion;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "document_id",
        nullable = false
    )
    Document document;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "artifact_id",
        nullable = false)
    Artifact artifact;

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
