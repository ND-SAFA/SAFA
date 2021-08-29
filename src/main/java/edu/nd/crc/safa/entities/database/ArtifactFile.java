package edu.nd.crc.safa.entities.database;

import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

/**
 * Responsible for mapping which TIM files
 */
@Entity
@Table(name = "artifact_file")
public class ArtifactFile {

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "file_id")
    UUID FileId;

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

    @Column(name = "fileName", nullable = false)
    String fileName;

    public ArtifactFile() {
    }

    public ArtifactFile(Project project,
                        ArtifactType artifactType,
                        String fileName) {
        this.project = project;
        this.artifactType = artifactType;
        this.fileName = fileName;
    }
}
