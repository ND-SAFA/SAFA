package edu.nd.crc.safa.entities;

import java.io.Serializable;
import java.util.UUID;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name = "projects")
public class Project implements Serializable {

    @Id
    @GeneratedValue
    @Column(name = "project_id")
    UUID projectId;

    @Column(name = "name")
    String name;

    public Project() {
    }

    public Project(String name) {
        this.setName(name);
    }

    public void setName(String name) {
        this.name = name;
    }

    public UUID getProjectId() {
        return this.projectId;
    }

    public String getName() {
        return this.name;
    }
}
