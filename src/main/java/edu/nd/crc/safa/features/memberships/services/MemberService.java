package edu.nd.crc.safa.features.memberships.services;

import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.memberships.entities.app.ProjectMemberAppEntity;
import edu.nd.crc.safa.features.memberships.entities.db.ProjectMembership;
import edu.nd.crc.safa.features.memberships.repositories.ProjectMembershipRepository;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.ProjectRole;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.repositories.SafaUserRepository;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.PathVariable;

/**
 * Responsible for CRUD operations related to project memberships
 */
@Service
@AllArgsConstructor
public class MemberService implements IAppEntityService<ProjectMemberAppEntity> {

    SafaUserRepository safaUserRepository;
    SafaUserService safaUserService;
    ProjectMembershipRepository projectMembershipRepository;

    /**
     * Retrieve project membership with given id. Throws error if not found.
     *
     * @param projectMembershipId ID of membership being retrieved.
     * @return The project membership.
     */
    public ProjectMembership getMembershipById(UUID projectMembershipId) {
        Optional<ProjectMembership> projectMembershipQuery =
            this.projectMembershipRepository.findById(projectMembershipId);
        if (projectMembershipQuery.isEmpty()) {
            throw new SafaError("Could not find membership with id: %s", projectMembershipId);
        }
        return projectMembershipQuery.get();
    }

    @Override
    public List<ProjectMemberAppEntity> getAppEntities(ProjectVersion projectVersion) {
        Project project = projectVersion.getProject();
        return this.projectMembershipRepository.findByProject(project)
            .stream()
            .map(ProjectMemberAppEntity::new)
            .collect(Collectors.toList());
    }

    /**
     * Finds and adds given member to project with specified role.
     *
     * @param project        The project to add the member to.
     * @param newMemberEmail The email of the member being added.
     * @param newMemberRole  The role to give the member in the project.
     * @return {@link ProjectMembership} Updated project membership.
     * @throws SafaError Throws error if given role is greater than the role
     *                   of the user issuing this request.
     */
    public ProjectMembership addOrUpdateProjectMembership(Project project,
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
        ProjectMembership updatedProjectMembership;
        if (projectMembershipQuery.isPresent()) {
            ProjectMembership existingProjectMembership = projectMembershipQuery.get();
            existingProjectMembership.setRole(newMemberRole);
            updatedProjectMembership = existingProjectMembership;
        } else {
            ProjectMembership newProjectMembership = new ProjectMembership(project, newMember, newMemberRole);
            updatedProjectMembership = newProjectMembership;
        }
        this.projectMembershipRepository.save(updatedProjectMembership);
        return updatedProjectMembership;
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
