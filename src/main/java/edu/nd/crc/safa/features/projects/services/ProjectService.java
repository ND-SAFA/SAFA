package edu.nd.crc.safa.features.projects.services;

import java.io.IOException;
import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.memberships.services.ProjectMembershipService;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipAppEntity;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.organizations.services.TeamService;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectIdAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.repositories.ProjectRepository;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.utilities.FileUtilities;

import lombok.Setter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Lazy;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Service;

/**
 * Responsible for updating, deleting, and retrieving project identifiers.
 */
@Service
@Scope("singleton")
public class ProjectService {

    @Setter(onMethod = @__({@Autowired}))
    private ProjectRepository projectRepository;

    @Setter(onMethod = @__({@Autowired}))
    private TeamService teamService;

    @Setter(onMethod = @__({@Autowired, @Lazy}))
    private ProjectMembershipService projectMembershipService;

    /**
     * Deletes given project and all related entities through cascade property.
     *
     * @param project The project to delete.
     * @throws SafaError Throws error if error occurs while deleting flat files.
     */
    public void deleteProject(Project project) throws SafaError, IOException {
        this.projectRepository.delete(project);
        FileUtilities.deletePath(ProjectPaths.Storage.projectPath(project, false));
    }

    /**
     * Creates a new project
     *
     * @param name The name of the project
     * @param description The description of the project
     * @param owner The team that owns the project
     * @return The new project
     */
    public Project createProject(String name, String description, Team owner) {
        Project project = new Project(name, description, owner);
        return this.projectRepository.save(project);
    }

    /**
     * Creates a new project
     *
     * @param name The name of the project
     * @param description The description of the project
     * @param owner The user that owns the project
     * @return The new project
     */
    public Project createProject(String name, String description, SafaUser owner) {
        Team personalTeam = teamService.getPersonalTeam(owner);
        return createProject(name, description, personalTeam);
    }

    /**
     * Creates a new project
     *
     * @param name The name of the project
     * @param description The description of the project
     * @param owner The organization that owns the project
     * @return The new project
     */
    public Project createProject(String name, String description, Organization owner) {
        Team orgTeam = teamService.getFullOrganizationTeam(owner);
        return createProject(name, description, orgTeam);
    }

    /**
     * Creates a new project
     *
     * @param projectDefinition The definition of the project from the front end
     * @param owner The user who will own the project
     * @return The new project
     */
    public Project createProject(ProjectAppEntity projectDefinition, SafaUser owner) {
        return createProject(projectDefinition.getName(), projectDefinition.getDescription(), owner);
    }

    /**
     * Creates a new project
     *
     * @param projectDefinition The definition of the project from the front end
     * @param owner The organization who will own the project
     * @return The new project
     */
    public Project createProject(ProjectAppEntity projectDefinition, Organization owner) {
        return createProject(projectDefinition.getName(), projectDefinition.getDescription(), owner);
    }

    /**
     * Creates a new project
     *
     * @param projectDefinition The definition of the project from the front end
     * @param owner The team who will own the project
     * @return The new project
     */
    public Project createProject(ProjectAppEntity projectDefinition, Team owner) {
        return createProject(projectDefinition.getName(), projectDefinition.getDescription(), owner);
    }

    /**
     * Return the list of projects that are owned by the specified team. This does not include
     * projects that are shared with the team.
     *
     * @param team The team
     * @return The projects the team owns
     */
    public List<Project> getProjectsOwnedByTeam(Team team) {
        return projectRepository.findByOwningTeam(team);
    }

    /**
     * Converts a project to a project identifier front-end object
     *
     * @param project The project
     * @return The project identifier
     */
    public ProjectIdAppEntity getIdAppEntity(Project project) {
        List<MembershipAppEntity> projectMemberships =
            projectMembershipService.getAllProjectMembers(project)
                .stream()
                .map(MembershipAppEntity::new)
                .collect(Collectors.toUnmodifiableList());
        return new ProjectIdAppEntity(project, projectMemberships);
    }

    /**
     * Converts a collection of projects to project identifiers
     *
     * @param projects The projects
     * @return A list of project identifier objects
     */
    public List<ProjectIdAppEntity> getIdAppEntities(Collection<Project> projects) {
        return projects.stream().map(this::getIdAppEntity).collect(Collectors.toUnmodifiableList());
    }
}
