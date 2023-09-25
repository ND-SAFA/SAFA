package edu.nd.crc.safa.features.projects.entities.db;

import java.io.Serializable;
import java.time.LocalDateTime;
import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.Lob;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;

import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
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
    private UUID projectId;

    /**
     * Name of project.
     */
    @Column(name = "name", nullable = false)
    private String name;

    /**
     * Description of project.
     * Lob to support GitHub repository descriptions
     */
    @Lob
    @Column(name = "description",
        nullable = false,
        columnDefinition = "mediumtext")
    private String description;

    @Lob
    @Column(name = "specification", columnDefinition = "mediumtext")
    private String specification;

    @Column(name = "last_edited")
    private LocalDateTime lastEdited;

    @JoinColumn(name = "team_id")
    @OnDelete(action = OnDeleteAction.CASCADE)
    @ManyToOne
    private Team owningTeam;

    public Project(String name, String description, Team owningTeam) {
        this.setName(name);
        this.setDescription(description);
        this.lastEdited = LocalDateTime.now();
        this.owningTeam = owningTeam;
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
        this.lastEdited = projectAppEntity.getLastEdited();
        if (this.lastEdited == null) {
            this.lastEdited = LocalDateTime.now();
        }
    }

    public void setLastEdited() {
        this.lastEdited = LocalDateTime.now();
    }
}
