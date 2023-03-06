package edu.nd.crc.safa.features.projects.services;

import java.io.IOException;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.memberships.entities.app.ProjectMemberAppEntity;
import edu.nd.crc.safa.features.memberships.entities.db.ProjectMembership;
import edu.nd.crc.safa.features.memberships.repositories.ProjectMembershipRepository;
import edu.nd.crc.safa.features.projects.entities.app.ProjectIdAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.repositories.ProjectRepository;
import edu.nd.crc.safa.features.users.entities.db.ProjectRole;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.utilities.FileUtilities;

import lombok.AllArgsConstructor;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Service;

/**
 * Responsible for updating, deleting, and retrieving project identifiers.
 */
@AllArgsConstructor
@Service
@Scope("singleton")
public class ProjectService {

    private final ProjectRepository projectRepository;
    private final ProjectMembershipRepository projectMembershipRepository;
    private final SafaUserService safaUserService;

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
     * Returns list of projects owned or shared with current user.
     *
     * @return List of projects where given user has access to.
     */
    public List<ProjectIdAppEntity> getProjectsForCurrentUser() {
        SafaUser user = this.safaUserService.getCurrentUser();
        return getProjectsForUser(user);
    }

    /**
     * Returns list of projects owned or shared with current user.
     *
     * @param user The user to get projects for
     * @return List of projects where given user has access to.
     */
    public List<ProjectIdAppEntity> getProjectsForUser(SafaUser user) {
        return this.projectMembershipRepository
            .findByMember(user)
            .stream()
            .map(ProjectMembership::getProject)
            .map(project -> {
                List<ProjectMemberAppEntity> members = this.projectMembershipRepository.findByProject(project)
                    .stream()
                    .map(ProjectMemberAppEntity::new)
                    .collect(Collectors.toList());
                return new ProjectIdAppEntity(project, members);
            })
            .collect(Collectors.toList());
    }

    /**
     * Sets authorized user as project owner and saves project.
     *
     * @param project The project to set user as owner
     */
    public void saveProjectWithCurrentUserAsOwner(Project project) {
        SafaUser user = this.safaUserService.getCurrentUser();
        saveProjectWithUserAsOwner(project, user);
    }

    /**
     * Sets authorized user as project owner and saves project.
     *
     * @param project The project to set user as owner
     * @param user The user to set as owner
     */
    public void saveProjectWithUserAsOwner(Project project, SafaUser user) {
        this.projectRepository.save(project);
        this.setUserAsOwner(project, user);
    }

    /**
     * The current authorized user to be an owner to given project.
     *
     * @param project The project the current user will be owner in.
     */
    public void setCurrentUserAsOwner(Project project) {
        SafaUser user = this.safaUserService.getCurrentUser();
        setUserAsOwner(project, user);
    }

    /**
     * The authorized user to be an owner to given project.
     *
     * @param project The project the current user will be owner in.
     * @param user The user to set as owner
     */
    public void setUserAsOwner(Project project, SafaUser user) {
        ProjectMembership projectMembership = new ProjectMembership(project, user, ProjectRole.OWNER);
        this.projectMembershipRepository.save(projectMembership);
    }
}
