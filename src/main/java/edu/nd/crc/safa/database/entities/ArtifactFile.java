package edu.nd.crc.safa.database.entities;

import java.util.UUID;

import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

/**
 * Responsible for mapping which TIM files
 */
@Entity
@Table(name = "artifact_file")
public class ArtifactFile {

    @Id
    @Column(name = "file_id")
    @GeneratedValue
    UUID FileId;

    @ManyToOne(cascade = CascadeType.REMOVE)
    @JoinColumn(
        name = "project_id",
        nullable = false
    )
    Project project;

    @ManyToOne(cascade = CascadeType.REMOVE)
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
