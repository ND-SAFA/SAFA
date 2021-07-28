package edu.nd.crc.safa.entities;

import java.io.Serializable;
import java.util.UUID;

import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

@Entity
@Table(name = "artifact_type")
public class ArtifactType implements Serializable {

    @Id
    @ManyToOne(cascade = CascadeType.REMOVE)
    @JoinColumn(
        name = "project_id"
    )
    Project projectId;

    @Id
    @Column(name = "type_id")
    @GeneratedValue
    UUID typeId;

    @Column(name = "name")
    String name;

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
        this.projectId = project;
    }
}
