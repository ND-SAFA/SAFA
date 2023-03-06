package edu.nd.crc.safa.features.users.services;

import java.util.Optional;

import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.memberships.entities.db.ProjectMembership;
import edu.nd.crc.safa.features.memberships.repositories.ProjectMembershipRepository;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.ProjectRole;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Provides api for adding members and verifying status within project.
 */
@Service
public class PermissionService {
    private final String PERMISSION_ERROR = "User does not have %s permissions for this project";
    private final ProjectMembershipRepository projectMembershipRepository;
    private final SafaUserService safaUserService;

    @Autowired
    public PermissionService(ProjectMembershipRepository projectMembershipRepository,
                             SafaUserService safaUserService) {
        this.projectMembershipRepository = projectMembershipRepository;
        this.safaUserService = safaUserService;
    }

    public void requireOwnerPermission(Project project) {
        SafaUser currentUser = this.safaUserService.getCurrentUser();
        requireOwnerPermission(project, currentUser);
    }

    public void requireOwnerPermission(Project project, SafaUser user) {
        if (!hasOwnerPermission(project, user)) {
            throw new SafaError(String.format(PERMISSION_ERROR, ProjectRole.OWNER));
        }
    }

    public void requireEditPermission(Project project) {
        SafaUser currentUser = this.safaUserService.getCurrentUser();
        requireEditPermission(project, currentUser);
    }

    public void requireEditPermission(Project project, SafaUser user) {
        if (!hasEditPermission(project, user)) {
            throw new SafaError(String.format(PERMISSION_ERROR, ProjectRole.EDITOR));
        }
    }

    public void requireViewPermission(Project project) {
        SafaUser currentUser = this.safaUserService.getCurrentUser();
        requireViewPermission(project, currentUser);
    }

    public void requireViewPermission(Project project, SafaUser user) {
        if (!hasViewingPermission(project, user)) {
            throw new SafaError(String.format(PERMISSION_ERROR, ProjectRole.VIEWER));
        }
    }

    private boolean hasOwnerPermission(Project project, SafaUser user) {
        return hasPermissionOrGreater(project, user, ProjectRole.OWNER);
    }

    private boolean hasEditPermission(Project project, SafaUser user) {
        return hasPermissionOrGreater(project, user, ProjectRole.EDITOR);
    }

    private boolean hasViewingPermission(Project project, SafaUser user) {
        return hasPermissionOrGreater(project, user, ProjectRole.VIEWER);
    }

    private boolean hasPermissionOrGreater(Project project, SafaUser user, ProjectRole role) {
        Optional<ProjectMembership> roleQuery = this.projectMembershipRepository.findByProjectAndMember(project, user);
        return roleQuery.filter(projectMembership -> projectMembership.getRole().compareTo(role) >= 0).isPresent();
    }

    public boolean hasViewPermission(JobDbEntity job, SafaUser user) {
        return job.getUser().getUserId().equals(user.getUserId());
    }
}
