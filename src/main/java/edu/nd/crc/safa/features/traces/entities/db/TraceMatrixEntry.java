package edu.nd.crc.safa.features.traces.entities.db;

import java.util.UUID;

import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

@Entity
@Table(name = "trace_matrix")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class TraceMatrixEntry {

    @Id
    @JdbcTypeCode(SqlTypes.BINARY)
    @GeneratedValue
    @Column
    private UUID id;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "project_version_id", nullable = false)
    private ProjectVersion projectVersion;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "source_type_id", nullable = false)
    private ArtifactType sourceType;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "target_type_id", nullable = false)
    private ArtifactType targetType;

    @Column
    private int count;

    @Column
    private int generatedCount;

    @Column
    private int approvedCount;

    public TraceMatrixEntry(ProjectVersion projectVersion, ArtifactType sourceType, ArtifactType targetType) {
        this.projectVersion = projectVersion;
        this.sourceType = sourceType;
        this.targetType = targetType;
        this.count = 0;
        this.generatedCount = 0;
        this.approvedCount = 0;
    }
}
