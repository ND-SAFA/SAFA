package edu.nd.crc.safa.server.services;

import java.util.Optional;

import edu.nd.crc.safa.server.authentication.SafaUserService;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectMembership;
import edu.nd.crc.safa.server.entities.db.ProjectRole;
import edu.nd.crc.safa.server.entities.db.SafaUser;
import edu.nd.crc.safa.server.repositories.ProjectMembershipRepository;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.SafaUserRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Provides api for adding members and verifying status within project.
 */
@Service
public class PermissionService {

    ProjectRepository projectRepository;
    SafaUserRepository safaUserRepository;
    ProjectMembershipRepository projectMembershipRepository;
    SafaUserService safaUserService;

    @Autowired
    public PermissionService(ProjectRepository projectRepository,
                             SafaUserRepository safaUserRepository,
                             ProjectMembershipRepository projectMembershipRepository,
                             SafaUserService safaUserService) {
        this.projectRepository = projectRepository;
        this.safaUserRepository = safaUserRepository;
        this.projectMembershipRepository = projectMembershipRepository;
        this.safaUserService = safaUserService;
    }

    public void requireViewPermission(Project project) throws SafaError {
        SafaUser currentUser = this.safaUserService.getCurrentUser();
        if (!hasViewingPermission(project, currentUser)) {
            throw new SafaError("User does not have edit permissions on project.");
        }
    }

    public void requireEditPermission(Project project) throws SafaError {
        SafaUser currentUser = this.safaUserService.getCurrentUser();
        if (!hasEditPermission(project, currentUser)) {
            throw new SafaError("User does not have edit permissions on project.");
        }
    }

    private boolean hasViewingPermission(Project project, SafaUser user) {
        return hasPermissionOrGreater(project, user, ProjectRole.VIEWER);
    }

    private boolean hasEditPermission(Project project, SafaUser user) {
        return hasPermissionOrGreater(project, user, ProjectRole.EDITOR);
    }

    private boolean hasAdminPermission(Project project, SafaUser user) {
        return hasPermissionOrGreater(project, user, ProjectRole.ADMIN);
    }

    private boolean hasPermissionOrGreater(Project project, SafaUser user, ProjectRole role) {
        Optional<ProjectMembership> roleQuery = this.projectMembershipRepository.findByProjectAndMember(project, user);
        roleQuery.ifPresent(projectMembership -> {
        });
        return roleQuery.filter(projectMembership -> projectMembership.getRole().compareTo(role) >= 0).isPresent();
    }
}
