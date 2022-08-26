package edu.nd.crc.safa.features.artifacts.entities.db;

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
import edu.nd.crc.safa.features.common.IBaseEntity;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.types.ArtifactType;

import lombok.Data;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

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
@Data
public class Artifact implements Serializable, IBaseEntity, IArtifact {

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

    @Override
    public UUID getBaseEntityId() {
        return this.artifactId;
    }
}
