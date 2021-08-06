package edu.nd.crc.safa.entities;

import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.ConstraintMode;
import javax.persistence.Entity;
import javax.persistence.ForeignKey;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;

/**
 * Responsible for storing which artifacts types
 * are traced in a project
 */
@Entity
@Table(name = "trace_matrix")
public class TraceMatrix {

    @Id
    @GeneratedValue
    @Column(name = "trace_matrix_id")
    UUID traceMatrixId;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "project_id",
        foreignKey = @ForeignKey(name = "project_id", value = ConstraintMode.PROVIDER_DEFAULT),
        nullable = false
    )
    Project project;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "source_type_id", nullable = false, referencedColumnName = "type_id")
    ArtifactType sourceType;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "target_type_id", nullable = false, referencedColumnName = "type_id")
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

    public ArtifactType getSourceType() {
        return this.sourceType;
    }

    public ArtifactType getTargetType() {
        return this.targetType;
    }
}
