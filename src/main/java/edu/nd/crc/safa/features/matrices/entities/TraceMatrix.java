package edu.nd.crc.safa.features.matrices.entities;

import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;
import javax.persistence.UniqueConstraint;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.config.AppConstraints;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.types.ArtifactType;

import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

/**
 * Represents the entity for storing a unique trace direction in a project
 * between two artifact types.
 */
@Entity
@Table(name = "trace_matrix",
    uniqueConstraints = {
        @UniqueConstraint(columnNames = {
            "project_id", "source_type_id", "target_type_id"
        }, name = AppConstraints.UNIQUE_TRACE_MATRIX_PER_PROJECT)
    }
)
public class TraceMatrix {

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "trace_matrix_id")
    @NotNull
    UUID traceMatrixId;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "project_id", nullable = false)
    Project project;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "source_type_id",
        referencedColumnName = "type_id",
        nullable = false
    )
    ArtifactType sourceArtifactType;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "target_type_id",
        referencedColumnName = "type_id",
        nullable = false
    )
    ArtifactType targetArtifactType;

    public TraceMatrix() {
    }

    public TraceMatrix(Project project, ArtifactType sourceArtifactType, ArtifactType targetArtifactType) {
        this.project = project;
        this.sourceArtifactType = sourceArtifactType;
        this.targetArtifactType = targetArtifactType;
    }

    public ArtifactType getSourceArtifactType() {
        return sourceArtifactType;
    }

    public void setSourceArtifactType(ArtifactType sourceArtifactType) {
        this.sourceArtifactType = sourceArtifactType;
    }

    public ArtifactType getTargetArtifactType() {
        return targetArtifactType;
    }

    public void setTargetArtifactType(ArtifactType targetArtifactType) {
        this.targetArtifactType = targetArtifactType;
    }

    public UUID getTraceMatrixId() {
        return traceMatrixId;
    }

    public void setTraceMatrixId(UUID traceMatrixId) {
        this.traceMatrixId = traceMatrixId;
    }

    public Project getProject() {
        return project;
    }

    public void setProject(Project project) {
        this.project = project;
    }

    public String toString() {
        return String.format("%s-%s",
            this.sourceArtifactType.getName(),
            this.targetArtifactType.getName());
    }
}
