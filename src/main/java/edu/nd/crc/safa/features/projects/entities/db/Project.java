package edu.nd.crc.safa.features.projects.entities.db;

import java.io.Serializable;
import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Lob;
import javax.persistence.Table;

import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;

import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.Type;

/**
 * Responsible for uniquely identifying which
 * projects exist.
 */
@Entity
@Table(name = "project")
@NoArgsConstructor
@Data
public class Project implements Serializable {

    /**
     * Unique identifier for project.
     */
    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "project_id")
    UUID projectId;
    /**
     * Name of project.
     */
    @Column(name = "name", nullable = false)
    String name;
    /**
     * Description of project.
     * Lob to support GitHub repository descriptions
     */
    @Lob
    @Column(name = "description",
        nullable = false,
        columnDefinition = "mediumtext")
    String description;

    public Project(String name, String description) {
        this.setName(name);
        this.setDescription(description);
    }

    /**
     * Creates project entity copying overlapping fields from given entity.
     *
     * @param projectAppEntity The project whose fields are copied.
     * @return Newly created project.
     */
    public static Project fromAppEntity(ProjectAppEntity projectAppEntity) {
        Project project = new Project();
        project.updateFromAppEntity(projectAppEntity);
        return project;
    }

    /**
     * Sets the overlapping fields in given entity.
     *
     * @param projectAppEntity The project to update from.
     */
    public void updateFromAppEntity(ProjectAppEntity projectAppEntity) {
        if (!(projectAppEntity.getProjectId() == null)) {
            this.projectId = projectAppEntity.getProjectId();
        }
        this.name = projectAppEntity.getName();
        this.description = projectAppEntity.getDescription();
    }
}
