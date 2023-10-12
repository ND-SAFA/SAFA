package edu.nd.crc.safa.features.artifacts.entities.db;

import java.io.Serializable;
import java.util.UUID;

import edu.nd.crc.safa.config.AppConstraints;
import edu.nd.crc.safa.features.common.IBaseEntity;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import jakarta.persistence.UniqueConstraint;
import lombok.Data;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

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
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column(name = "artifact_id")
    private UUID artifactId;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "project_id",
        nullable = false
    )
    private Project project;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "type_id",
        nullable = false)
    private ArtifactType type;

    @Column(name = "name")
    private String name;

    @Enumerated(EnumType.STRING)
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column(name = "document_type")
    private DocumentType documentType;

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
