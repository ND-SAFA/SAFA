package edu.nd.crc.safa.features.projects.entities.app;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.memberships.entities.app.ProjectMemberAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.ProjectRole;

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
    String projectId;
    /**
     * The name of the project.
     */
    String name;
    /**
     * The description of the project.
     */
    String description;
    /**
     * The project owner email.
     */
    String owner;
    /**
     * List of member on project.
     */
    List<ProjectMemberAppEntity> members;

    public ProjectIdAppEntity(Project project, List<ProjectMemberAppEntity> members) {
        this.projectId = project.getProjectId().toString();
        this.name = project.getName();
        this.description = project.getDescription();
        this.members = members;
        this.owner = getProjectOwner();
    }

    private String getProjectOwner() {
        List<ProjectMemberAppEntity> ownerQuery =
            members
                .stream()
                .filter(m -> m.getRole() == ProjectRole.OWNER)
                .collect(Collectors.toList());
        if (ownerQuery.isEmpty()) {
            return null;
        } else {
            return ownerQuery.get(0).getEmail();
        }
    }
}
