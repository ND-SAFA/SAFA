package edu.nd.crc.safa.server.entities.db;

import java.io.Serializable;
import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;
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
import org.json.JSONObject;

/**
 * Responsible for storing the unique identifiers for artifacts
 * in a project.
 */
@Entity
@Table(name = "artifact",
    uniqueConstraints = {
        @UniqueConstraint(
            columnNames = {
                "project_id",
                "name"
            }, name = AppConstraints.UNIQUE_ARTIFACT_NAME_PER_PROJECT)
    })
public class Artifact implements Serializable, IBaseEntity {

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "artifact_id")
    UUID artifactId;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "project_id",
        nullable = false
    )
    Project project;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "type_id",
        nullable = false)
    ArtifactType type;

    @Column(name = "name")
    String name;
    @Column(name = "document_type")
    @Enumerated(EnumType.STRING)
    DocumentType documentType;

    public Artifact() {
        this.documentType = DocumentType.ARTIFACT_TREE;
    }

    public Artifact(Project project, ArtifactType type, String name, DocumentType documentType) {
        this();
        this.project = project;
        this.type = type;
        this.name = name;
        this.documentType = documentType;
    }

    public DocumentType getDocumentType() {
        return documentType;
    }

    public void setDocumentType(DocumentType documentType) {
        this.documentType = documentType;
    }

    public Project getProject() {
        return this.project;
    }

    public void setProject(Project project) {
        this.project = project;
    }

    public ArtifactType getType() {
        return this.type;
    }

    public void setType(ArtifactType artifactType) {
        this.type = artifactType;
    }

    public String getBaseEntityId() {
        return this.artifactId.toString();
    }

    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public UUID getArtifactId() {
        return this.artifactId;
    }

    public String toString() {
        JSONObject json = new JSONObject();
        json.put("name", this.name);
        json.put("docType", this.documentType);
        return json.toString();
    }
}
