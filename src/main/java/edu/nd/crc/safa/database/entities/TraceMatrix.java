package edu.nd.crc.safa.database.entities;

import java.util.UUID;

import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.ConstraintMode;
import javax.persistence.Entity;
import javax.persistence.ForeignKey;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

/**
 * Responsible for storing which artifacts types
 * are traced in a project
 */
@Entity
@Table(name = "trace_matrix")
public class TraceMatrix {

    @Id
    @Column(name = "trace_matrix_id")
    UUID traceMatrixId;

    @ManyToOne(cascade = CascadeType.REMOVE)
    @JoinColumn(
        name = "project_id",
        foreignKey = @ForeignKey(name = "project_id", value = ConstraintMode.PROVIDER_DEFAULT),
        nullable = false
    )
    Project project;

    @ManyToOne
    @JoinColumn(name = "type_id", nullable = false)
    ArtifactType sourceType;

    @ManyToOne
    @JoinColumn(name = "type_id", nullable = false)
    ArtifactType targetType;

    @Column(name = "is_generated", nullable = false)
    boolean isGenerated;

    public TraceMatrix() {
    }

    public TraceMatrix(Project project,
                       ArtifactType sourceType,
                       ArtifactType targetType,
                       boolean isGenerated) {
        this.project = project;
        this.sourceType = sourceType;
        this.targetType = targetType;
        this.isGenerated = isGenerated;
    }
}
