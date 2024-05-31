package edu.nd.crc.safa.features.artifacts.entities.db;

import java.io.Serializable;
import java.util.UUID;

import edu.nd.crc.safa.config.AppConstraints;
import edu.nd.crc.safa.features.common.IBaseEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
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

    @Column(nullable = false)
    @JdbcTypeCode(SqlTypes.VARCHAR)
    private UUID projectId;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "type_id",
        nullable = false)
    private ArtifactType type;

    @Column(name = "name")
    private String name;

    public Artifact() {
    }

    public Artifact(Project project, ArtifactType type, String name) {
        this();
        this.projectId = project.getId();
        this.type = type;
        this.name = name;
    }

    @Override
    public UUID getBaseEntityId() {
        return this.artifactId;
    }
}
