package edu.nd.crc.safa.server.services;

import java.util.Optional;

import edu.nd.crc.safa.server.authentication.SafaUserService;
import edu.nd.crc.safa.server.entities.api.ServerError;
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

    public void requireEditPermission(Project project) throws ServerError {
        SafaUser currentUser = this.safaUserService.getCurrentUser();
        if (!hasEditPermission(project, currentUser)) {
            throw new ServerError("User does not have edit permissions on project.");
        }
    }

    public void requireViewPermission(Project project) throws ServerError {
        SafaUser currentUser = this.safaUserService.getCurrentUser();
        if (!hasViewingPermission(project, currentUser)) {
            throw new ServerError("User does not have edit permissions on project.");
        }
    }

    private boolean hasViewingPermission(Project project, SafaUser user) {
        Optional<ProjectMembership> roleQuery = this.projectMembershipRepository.findByProjectAndMember(project, user);
        return roleQuery.isPresent() || isOwner(project, user);
    }

    private boolean hasEditPermission(Project project, SafaUser user) {
        Optional<ProjectMembership> roleQuery = this.projectMembershipRepository.findByProjectAndMember(project, user);
        return roleQuery.filter(projectMembership -> projectMembership.getRole() != ProjectRole.VIEWER).isPresent()
            || isOwner(project, user);
    }

    private boolean hasAdminPermission(Project project, SafaUser user) {
        Optional<ProjectMembership> roleQuery = this.projectMembershipRepository.findByProjectAndMember(project, user);
        boolean isAdmin =
            roleQuery.filter(projectMembership -> projectMembership.getRole() == ProjectRole.ADMIN).isPresent();
        return isAdmin || isOwner(project, user);
    }

    public boolean isOwner(Project project, SafaUser user) {
        return project.getOwner().getUserId().equals(user.getUserId());
    }
}
