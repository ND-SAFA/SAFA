package edu.nd.crc.safa.database.entities;

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
import javax.persistence.ManyToOne;
import javax.persistence.Table;

/**
 * Responsible for identifying each project's version.
 */
@Entity
@Table(name = "project_versions")
public class ProjectVersion implements Serializable {

    @Id
    @Column(name = "version_id")
    @GeneratedValue
    UUID versionId; //todo: generate in sequence relative to project id using GenericGenerator

    @ManyToOne(cascade = CascadeType.REMOVE)
    @JoinColumn(
        name = "project_id",
        foreignKey = @ForeignKey(value = ConstraintMode.PROVIDER_DEFAULT),
        nullable = false
    )
    Project project;


    public ProjectVersion() {
    }

    public ProjectVersion(Project project) {
        this.project = project;
    }
}
