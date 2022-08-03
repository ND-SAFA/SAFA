package edu.nd.crc.safa.features.projects.services;

import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.authentication.SafaUserService;
import edu.nd.crc.safa.features.projects.entities.app.ProjectIdentifier;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.app.ProjectMemberAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.ProjectMembership;
import edu.nd.crc.safa.features.users.entities.db.ProjectRole;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.repositories.ProjectMembershipRepository;
import edu.nd.crc.safa.features.projects.repositories.ProjectRepository;
import edu.nd.crc.safa.features.versions.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.features.users.repositories.SafaUserRepository;
import edu.nd.crc.safa.utilities.OSHelper;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.PathVariable;

/**
 * Responsible for updating, deleting, and retrieving project identifiers.
 */
@Service
@Scope("singleton")
public class ProjectService {

    private final ProjectRepository projectRepository;
    private final ProjectVersionRepository projectVersionRepository;
    private final ProjectMembershipRepository projectMembershipRepository;
    private final SafaUserRepository safaUserRepository;

    private final SafaUserService safaUserService;

    @Autowired
    public ProjectService(ProjectRepository projectRepository,
                          ProjectVersionRepository projectVersionRepository,
                          ProjectMembershipRepository projectMembershipRepository,
                          SafaUserRepository safaUserRepository,
                          SafaUserService safaUserService) {
        this.projectRepository = projectRepository;
        this.projectVersionRepository = projectVersionRepository;
        this.projectMembershipRepository = projectMembershipRepository;
        this.safaUserRepository = safaUserRepository;
        this.safaUserService = safaUserService;
    }

    /**
     * Deletes given project and all related entities through cascade property.
     *
     * @param project The project to delete.
     * @throws SafaError Throws error if error occurs while deleting flat files.
     */
    public void deleteProject(Project project) throws SafaError {
        this.projectRepository.delete(project);
        OSHelper.deletePath(ProjectPaths.getPathToStorage(project, false));
    }

    /**
     * Returns list of projects owned or shared with current user.
     *
     * @return List of projects where given user has access to.
     */
    public List<ProjectIdentifier> getCurrentUserProjects() {
        SafaUser user = this.safaUserService.getCurrentUser();
        return this.projectMembershipRepository
            .findByMember(user)
            .stream()
            .map(ProjectMembership::getProject)
            .map(project -> {
                List<ProjectMemberAppEntity> members = this.projectMembershipRepository.findByProject(project)
                    .stream()
                    .map(ProjectMemberAppEntity::new)
                    .collect(Collectors.toList());
                return new ProjectIdentifier(project, members);
            })
            .collect(Collectors.toList());
    }

    public void saveProjectWithCurrentUserAsOwner(Project project) {
        this.projectRepository.save(project);
        this.setCurrentUserAsOwner(project);
    }

    public ProjectVersion createInitialProjectVersion(Project project) {
        ProjectVersion projectVersion = new ProjectVersion(project, 1, 1, 1);
        this.projectVersionRepository.save(projectVersion);
        projectVersion.setProject(project);
        return projectVersion;
    }

    /**
     * Finds and adds given member to project with specified role.
     *
     * @param project        The project to add the member to.
     * @param newMemberEmail The email of the member being added.
     * @param newMemberRole  The role to give the member in the project.
     * @throws SafaError Throws error if given role is greater than the role
     *                   of the user issuing this request.
     */
    public void addOrUpdateProjectMembership(Project project,
                                             String newMemberEmail,
                                             ProjectRole newMemberRole) throws SafaError {
        // Step - Find member being added and the current member.
        Optional<SafaUser> newMemberQuery = this.safaUserRepository.findByEmail(newMemberEmail);
        if (newMemberQuery.isEmpty()) {
            throw new SafaError("No user exists with given email: " + newMemberEmail);
        }
        SafaUser newMember = newMemberQuery.get();
        SafaUser currentUser = this.safaUserService.getCurrentUser();

        // Step - Assert that member being added has fewer permissions than current user.
        Optional<ProjectMembership> currentUserMembershipQuery = this.projectMembershipRepository
            .findByProjectAndMember(project, currentUser);
        if (currentUserMembershipQuery.isPresent()) {
            if (newMemberRole.compareTo(currentUserMembershipQuery.get().getRole()) > 0) {
                throw new SafaError("Cannot add member with authorization greater that current user.");
            }
        } else {
            throw new SafaError("Cannot add member to project which current user is not apart of.");
        }

        Optional<ProjectMembership> projectMembershipQuery =
            this.projectMembershipRepository.findByProjectAndMember(project, newMember);
        if (projectMembershipQuery.isPresent()) {
            ProjectMembership existingProjectMembership = projectMembershipQuery.get();
            existingProjectMembership.setRole(newMemberRole);
            this.projectMembershipRepository.save(existingProjectMembership);
        } else {
            ProjectMembership newProjectMembership = new ProjectMembership(project, newMember, newMemberRole);
            this.projectMembershipRepository.save(newProjectMembership);
        }
    }

    /**
     * Returns list of members in given project.
     *
     * @param project The project whose members are retrieved.
     * @return List of project memberships relating members to projects.
     */
    public List<ProjectMembership> getProjectMembers(Project project) {
        return this.projectMembershipRepository.findByProject(project);
    }

    /**
     * The current authorized user to be an owner to given project.
     *
     * @param project The project the current user will be owner in.
     */
    public void setCurrentUserAsOwner(Project project) {
        SafaUser user = this.safaUserService.getCurrentUser();
        ProjectMembership projectMembership = new ProjectMembership(project, user, ProjectRole.OWNER);
        this.projectMembershipRepository.save(projectMembership);
    }

    /**
     * Deletes project membership effectively removing user from
     * associated project
     *
     * @param projectMembershipId ID of the membership linking user and project.
     * @return ProjectMembers The membership object identified by given id, or null if none found.
     */
    public ProjectMembership deleteProjectMembershipById(@PathVariable UUID projectMembershipId) {
        Optional<ProjectMembership> projectMembershipQuery =
            this.projectMembershipRepository.findById(projectMembershipId);
        if (projectMembershipQuery.isPresent()) {
            ProjectMembership projectMembership = projectMembershipQuery.get();
            this.projectMembershipRepository.delete(projectMembership);
            return projectMembership;
        }
        return null;
    }
}
