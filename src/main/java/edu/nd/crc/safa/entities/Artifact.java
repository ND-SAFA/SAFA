package edu.nd.crc.safa.entities;

import java.io.Serializable;
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
@Table(name = "artifacts")
public class Artifact implements Serializable {

    @Id
    @Column(name = "artifact_id")
    @GeneratedValue
    UUID artifactId;

    @ManyToOne(cascade = CascadeType.REMOVE)
    @JoinColumn(
        name = "project_id",
        foreignKey = @ForeignKey(name = "project_id", value = ConstraintMode.PROVIDER_DEFAULT),
        nullable = false
    )
    Project projectId;

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
    ArtifactType type;

    @Column(name = "name")
    String name;
}
