package edu.nd.crc.safa.entities.database;

import java.io.Serializable;
import javax.persistence.Column;
import javax.persistence.ConstraintMode;
import javax.persistence.Entity;
import javax.persistence.ForeignKey;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;

/**
 * Responsible for identifying each project's version.
 */
@Entity
@Table(name = "project_versions")
public class ProjectVersion implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE)
    @Column(name = "version_id")
    long versionId; //todo: generate in sequence relative to project id using GenericGenerator

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
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

    public Project getProject() {
        return this.project;
    }
}
