package edu.nd.crc.safa.entities;

import java.io.Serializable;
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

/**
 * Responsible for defining which types are available
 * to which projects.
 */
@Entity
@Table(name = "artifact_type")
public class ArtifactType implements Serializable {

    @Id
    @Column(name = "type_id")
    @GeneratedValue
    UUID typeId;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "project_id",
        nullable = false
    )
    Project project;

    @Column(name = "name")
    String name;

    public ArtifactType() {
    }

    public ArtifactType(Project project, String name) {
        this.project = project;
        this.name = name.toLowerCase();
    }

    public UUID getTypeId() {
        return this.typeId;
    }

    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name.toLowerCase();
    }

    public void setProject(Project project) {
        this.project = project;
    }
}
