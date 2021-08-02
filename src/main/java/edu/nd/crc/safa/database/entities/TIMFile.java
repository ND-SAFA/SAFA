package edu.nd.crc.safa.database.entities;

import java.util.UUID;

import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.ConstraintMode;
import javax.persistence.Entity;
import javax.persistence.ForeignKey;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.JoinColumns;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

@Entity
@Table(name = "tim_file")
public class TIMFile {

    @Id
    @Column(name = "file_id")
    @GeneratedValue
    UUID FileId;

    @ManyToOne(cascade = CascadeType.REMOVE)
    @JoinColumn(
        name = "project_id",
        foreignKey = @ForeignKey(name = "project_id", value = ConstraintMode.PROVIDER_DEFAULT),
        nullable = false
    )
    Project project;

    @ManyToOne(cascade = CascadeType.REMOVE)
    @JoinColumns({
        @JoinColumn(
            name = "type_project_id",
            nullable = false,
            referencedColumnName = "project_id" //TODO: Figure out if this can ever mismatch with project_id above
        ),
        @JoinColumn(
            name = "type_id",
            nullable = false,
            referencedColumnName = "type_id"
        )
    })
    ArtifactType artifactType;

    @Column(name = "fileName")
    String fileName;

    public TIMFile(Project project,
                   ArtifactType artifactType,
                   String fileName) {
        this.project = project;
        this.artifactType = artifactType;
        this.fileName = fileName;
    }
}
