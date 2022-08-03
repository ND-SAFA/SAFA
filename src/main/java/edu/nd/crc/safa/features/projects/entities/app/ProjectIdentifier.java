package edu.nd.crc.safa.features.projects.entities.app;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.users.entities.app.ProjectMemberAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.ProjectRole;

/**
 * Responsible for including information regarding project
 * selection.
 */
public class ProjectIdentifier {

    String projectId;
    String name;
    String description;
    String owner;
    List<ProjectMemberAppEntity> members;

    public ProjectIdentifier() {
    }

    public ProjectIdentifier(Project project, List<ProjectMemberAppEntity> members) {
        this.projectId = project.getProjectId().toString();
        this.name = project.getName();
        this.description = project.getDescription();
        this.members = members;
        List<ProjectMemberAppEntity> ownerQuery =
            members
                .stream()
                .filter(m -> m.getRole() == ProjectRole.OWNER)
                .collect(Collectors.toList());
        this.owner = ownerQuery.get(0).getEmail();
    }

    public String getProjectId() {
        return projectId;
    }

    public void setProjectId(String projectId) {
        this.projectId = projectId;
    }

    public String getOwner() {
        return owner;
    }

    public void setOwner(String owner) {
        this.owner = owner;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public List<ProjectMemberAppEntity> getMembers() {
        return members;
    }

    public void setMembers(List<ProjectMemberAppEntity> members) {
        this.members = members;
    }
}
