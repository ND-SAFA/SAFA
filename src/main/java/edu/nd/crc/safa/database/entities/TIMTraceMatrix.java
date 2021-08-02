package edu.nd.crc.safa.database.entities;

import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.ConstraintMode;
import javax.persistence.Entity;
import javax.persistence.ForeignKey;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

/**
 * Responsible for storing which artifacts types
 * are traced in a project
 */
@Entity
@Table(name = "tim_trace_matrix")
public class TIMTraceMatrix {
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
}
