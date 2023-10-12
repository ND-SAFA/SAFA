package edu.nd.crc.safa.features.projects.entities.app;

import java.time.LocalDateTime;
import java.util.List;

import edu.nd.crc.safa.features.organizations.entities.app.MembershipAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Responsible for including information regarding project
 * selection.
 */
@NoArgsConstructor
@Data
public class ProjectIdAppEntity {
    /**
     * The ID of the project.
     */
    private String projectId;
    /**
     * The name of the project.
     */
    private String name;
    /**
     * The description of the project.
     */
    private String description;
    /**
     * The owning team ID.
     */
    private String owner;
    /**
     * List of member on project.
     */
    private List<MembershipAppEntity> members;
    /**
     * Last edited.
     */
    private LocalDateTime lastEdited;
    private List<String> permissions;

    public ProjectIdAppEntity(Project project, List<MembershipAppEntity> members, List<String> permissions) {
        this.projectId = project.getProjectId().toString();
        this.name = project.getName();
        this.description = project.getDescription();
        this.members = members;
        this.owner = project.getOwningTeam().getId().toString();
        this.lastEdited = project.getLastEdited();
        this.permissions = permissions;
    }
}
