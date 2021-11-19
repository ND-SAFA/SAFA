package edu.nd.crc.safa.server.entities.db;

import java.io.Serializable;
import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;

import edu.nd.crc.safa.server.entities.app.ProjectAppEntity;

import org.hibernate.annotations.Type;
import org.json.JSONObject;

/**
 * Responsible for uniquely identifying which
 * projects exist.
 */
@Entity
@Table(name = "project")
public class Project implements Serializable {

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "project_id")
    UUID projectId;

    @Column(name = "name")
    String name;

    @Column(name = "description")
    String description;

    public Project() {
    }

    public Project(String name, String description) {
        this.setName(name);
        this.setDescription(description);
    }

    public static Project fromAppEntity(ProjectAppEntity appEntity) {
        Project project = new Project();
        if (appEntity.getProjectId() != null && !appEntity.getProjectId().equals("")) {
            project.projectId = UUID.fromString(appEntity.getProjectId());
        }
        project.name = appEntity.getName();
        project.description = appEntity.getDescription();
        return project;
    }

    public UUID getProjectId() {
        return this.projectId;
    }

    public void setProjectId(UUID projectId) {
        this.projectId = projectId;
    }

    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDescription() {
        return this.description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public boolean hasDefinedId() {
        return this.projectId != null && !this.projectId.toString().equals("");
    }

    public String toString() {
        JSONObject json = new JSONObject();
        json.put("projectId", projectId);
        json.put("name", name);
        return json.toString();
    }
}
