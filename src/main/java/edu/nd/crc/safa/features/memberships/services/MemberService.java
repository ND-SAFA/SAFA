package edu.nd.crc.safa.features.memberships.services;

import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.memberships.entities.app.ProjectMemberAppEntity;
import edu.nd.crc.safa.features.memberships.entities.db.UserProjectMembership;
import edu.nd.crc.safa.features.memberships.repositories.UserProjectMembershipRepository;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
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
    UserProjectMembershipRepository userProjectMembershipRepository;

    /**
     * Retrieve project membership with given id. Throws error if not found.
     *
     * @param projectMembershipId ID of membership being retrieved.
     * @return The project membership.
     */
    public UserProjectMembership getMembershipById(UUID projectMembershipId) {
        Optional<UserProjectMembership> projectMembershipQuery =
            this.userProjectMembershipRepository.findById(projectMembershipId);
        if (projectMembershipQuery.isEmpty()) {
            throw new SafaError("Could not find membership with id: %s.", projectMembershipId);
        }
        return projectMembershipQuery.get();
    }

    @Override
    public List<ProjectMemberAppEntity> getAppEntities(ProjectVersion projectVersion, SafaUser user) {
        Project project = projectVersion.getProject();
        return this.userProjectMembershipRepository.findByProject(project)
            .stream()
            .map(ProjectMemberAppEntity::new)
            .collect(Collectors.toList());
    }

    /**
     * Finds and adds given member to project with specified role.
     *
     * @param project        The project to add the member to.
     * @param currentUser    The user performing the update.
     * @param newMemberEmail The email of the member being added.
     * @param newMemberRole  The role to give the member in the project.
     * @return {@link UserProjectMembership} Updated project membership.
     * @throws SafaError Throws error if given role is greater than the role
     *                   of the user issuing this request.
     */
    public UserProjectMembership addOrUpdateProjectMembership(Project project, SafaUser currentUser,
                                                              String newMemberEmail,
                                                              ProjectRole newMemberRole) throws SafaError {
        // Step - Find member being added and the current member.
        SafaUser newMember = this.safaUserService.getUserByEmail(newMemberEmail);

        // Step - Assert that member being added has fewer permissions than current user.
        List<UserProjectMembership> projectMemberships = this.userProjectMembershipRepository.findByProject(project);
        if (projectMemberships.size() == 1
            && projectMemberships.get(0).getMember().getEmail().equals(newMemberEmail)) {
            throw new SafaError("Unable to edit permission of only member of project.");
        }
        long nOwners = projectMemberships.stream().filter(pm -> pm.getRole().equals(ProjectRole.OWNER)).count();

        // Step - Validate current user
        validateCurrentUserPermissions(newMemberRole, currentUser, projectMemberships);

        // Step - Create or update project membership
        Optional<UserProjectMembership> projectMembershipQuery =
            this.userProjectMembershipRepository.findByProjectAndMember(project, newMember);
        UserProjectMembership updatedProjectMembership;
        if (projectMembershipQuery.isPresent()) {
            UserProjectMembership existingProjectMembership = projectMembershipQuery.get();
            if (existingProjectMembership.getRole().equals(ProjectRole.OWNER) && nOwners == 1) {
                throw new SafaError("Cannot edit role of last project owner.");
            }
            existingProjectMembership.setRole(newMemberRole);
            updatedProjectMembership = existingProjectMembership;
        } else {
            updatedProjectMembership = new UserProjectMembership(project, newMember, newMemberRole);
        }

        // Step - Save changes
        this.userProjectMembershipRepository.save(updatedProjectMembership);

        return updatedProjectMembership;
    }

    /**
     * Returns list of members in given project.
     *
     * @param project The project whose members are retrieved.
     * @return List of project memberships relating members to projects.
     */
    public List<UserProjectMembership> getProjectMembers(Project project) {
        return this.userProjectMembershipRepository.findByProject(project);
    }

    /**
     * Returns list of members in given project with any of the given roles.
     *
     * @param project The project whose members are retrieved.
     * @param projectRoles The project roles to match.
     * @return List of project memberships relating members to projects.
     */
    public List<UserProjectMembership> getProjectMembersWithRoles(Project project, List<ProjectRole> projectRoles) {
        return this.userProjectMembershipRepository.findByProjectAndRoleIn(project, projectRoles);
    }

    /**
     * Returns list of members in given project with the given role.
     *
     * @param project The project whose members are retrieved.
     * @param projectRole The project role to match.
     * @return List of project memberships relating members to projects.
     */
    public List<UserProjectMembership> getProjectMembersWithRole(Project project, ProjectRole projectRole) {
        return getProjectMembersWithRoles(project, List.of(projectRole));
    }

    /**
     * Deletes project membership effectively removing user from
     * associated project
     *
     * @param projectMembershipId ID of the membership linking user and project.
     * @return ProjectMembers The membership object identified by given id, or null if none found.
     */
    public UserProjectMembership deleteProjectMembershipById(@PathVariable UUID projectMembershipId) {
        Optional<UserProjectMembership> projectMembershipQuery =
            this.userProjectMembershipRepository.findById(projectMembershipId);
        if (projectMembershipQuery.isPresent()) {
            UserProjectMembership projectMembership = projectMembershipQuery.get();
            this.userProjectMembershipRepository.delete(projectMembership);
            return projectMembership;
        }
        return null;
    }

    private void validateCurrentUserPermissions(ProjectRole newMemberRole,
                                                SafaUser currentUser,
                                                List<UserProjectMembership> projectMemberships) {
        List<UserProjectMembership> currentUserMembershipQuery = projectMemberships
            .stream()
            .filter(pm -> pm.getMember().equals(currentUser))
            .collect(Collectors.toList());
        if (currentUserMembershipQuery.isEmpty()) {
            throw new SafaError("%s is not a member on project.", currentUser.getEmail());
        }
        UserProjectMembership currentUserMembership = currentUserMembershipQuery.get(0);
        if (newMemberRole.compareTo(currentUserMembership.getRole()) > 0) {
            throw new SafaError("Cannot add member with authorization greater that current user.");
        }
    }
}
