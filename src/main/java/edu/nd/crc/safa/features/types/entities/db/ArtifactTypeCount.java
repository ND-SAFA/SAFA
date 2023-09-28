package edu.nd.crc.safa.features.types.entities.db;

import java.util.UUID;

import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

@Entity
@Table(name = "type_counts")
@Getter
@Setter
@NoArgsConstructor
public class ArtifactTypeCount {

    @Id
    @JdbcTypeCode(SqlTypes.BINARY)
    @GeneratedValue
    @Column
    private UUID id;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "type_id", nullable = false)
    private ArtifactType type;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "project_version_id", nullable = false)
    private ProjectVersion projectVersion;

    @Column
    private int count;

    public ArtifactTypeCount(ProjectVersion projectVersion, ArtifactType type) {
        this.projectVersion = projectVersion;
        this.type = type;
        this.count = 0;
    }
}
