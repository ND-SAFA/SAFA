package edu.nd.crc.safa.features.artifacts.entities.db;

import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import edu.nd.crc.safa.features.projects.entities.db.Project;

import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

/**
 * Responsible for mapping which TIM files
 */
@Entity
@Table(name = "artifact_file")
@NoArgsConstructor
@Data
public class ArtifactFile {

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "file_id")
    UUID fileId;

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
        nullable = false
    )
    ArtifactType artifactType;

    @Column(name = "file_name", nullable = false)
    String fileName;
}
