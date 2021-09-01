package edu.nd.crc.safa.entities.sql;

import java.io.Serializable;
import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;

import edu.nd.crc.safa.entities.application.ProjectApplicationEntity;

import org.hibernate.annotations.Type;

/**
 * Responsible for uniquely identifying which
 * projects exist.
 */
@Entity
@Table(name = "projects")
public class Project implements Serializable {

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "project_id")
    UUID projectId;

    @Column(name = "name")
    String name;

    public Project() {
    }

    public Project(ProjectApplicationEntity appEntity) {
        if (appEntity.getProjectId() != null && !appEntity.getProjectId().equals("")) {
            this.projectId = UUID.fromString(appEntity.getProjectId());
        }
        this.name = appEntity.getName();
    }

    public Project(String name) {
        this.setName(name);
    }

    public UUID getProjectId() {
        return this.projectId;
    }

    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
