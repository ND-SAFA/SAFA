package edu.nd.crc.safa.features.traces.entities.db;

import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;

@Entity
@Table(name = "trace_matrix")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class TraceMatrixEntry {

    @Id
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
}
