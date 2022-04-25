package edu.nd.crc.safa.server.services;

import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.authentication.SafaUserService;
import edu.nd.crc.safa.server.entities.api.ProjectIdentifier;
import edu.nd.crc.safa.server.entities.api.ProjectVersionErrors;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.app.project.ProjectMemberAppEntity;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectMembership;
import edu.nd.crc.safa.server.entities.db.ProjectRole;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.SafaUser;
import edu.nd.crc.safa.server.repositories.projects.ProjectMembershipRepository;
import edu.nd.crc.safa.server.repositories.projects.ProjectRepository;
import edu.nd.crc.safa.server.repositories.projects.ProjectVersionRepository;
import edu.nd.crc.safa.server.repositories.projects.SafaUserRepository;
import edu.nd.crc.safa.utilities.OSHelper;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.PathVariable;

/**
 * Responsible for updating, deleting, and retrieving project identifiers.
 */
@Service
public class ProjectService {

    private final ProjectRepository projectRepository;
    private final ProjectVersionRepository projectVersionRepository;
    private final ProjectMembershipRepository projectMembershipRepository;
    private final SafaUserRepository safaUserRepository;

    private final SafaUserService safaUserService;
    private final EntityVersionService entityVersionService;

    @Autowired
    public ProjectService(ProjectRepository projectRepository,
                          ProjectVersionRepository projectVersionRepository,
                          ProjectMembershipRepository projectMembershipRepository,
                          SafaUserRepository safaUserRepository,
                          SafaUserService safaUserService,
                          EntityVersionService entityVersionService) {
        this.projectRepository = projectRepository;
        this.projectVersionRepository = projectVersionRepository;
        this.projectMembershipRepository = projectMembershipRepository;
        this.safaUserRepository = safaUserRepository;
        this.safaUserService = safaUserService;
        this.entityVersionService = entityVersionService;
    }

    /**
     * Deletes given project and all related entities through cascade property.
     *
     * @param project The project to delete.
     * @throws SafaError Throws error if error occurs while deleting flat files.
     */
    public void deleteProject(Project project) throws SafaError {
        this.projectRepository.delete(project);
        OSHelper.deletePath(ProjectPaths.getPathToStorage(project));
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

    public ProjectVersionErrors updateProjectAtVersion(Project project,
                                                       ProjectVersion projectVersion,
                                                       ProjectAppEntity payload) throws SafaError {
        ProjectVersionErrors response;
        Project persistentProject = this.projectRepository.findByProjectId(project.getProjectId());
        persistentProject.setName(project.getName());
        persistentProject.setDescription(project.getDescription());
        this.projectRepository.save(persistentProject);
        //TODO: Revisit why we have so many error checks.
        if (projectVersion == null) {
            if ((payload.artifacts != null
                && payload.artifacts.size() > 0)) {
                throw new SafaError("Cannot update artifacts because project version not defined");
            }
            response = new ProjectVersionErrors(payload, null, null, null);
        } else if (!projectVersion.hasValidId()) {
            throw new SafaError("Invalid Project version: must have a valid ID.");
        } else if (!projectVersion.hasValidVersion()) {
            throw new SafaError("Invalid Project version: must contain positive major, minor, and revision "
                + "numbers.");
        } else {
            projectVersion.setProject(project);
            this.projectVersionRepository.save(projectVersion);
            response = entityVersionService.setProjectEntitiesAtVersion(projectVersion,
                payload.getArtifacts(),
                payload.getTraces());
        }
        return response;
    }

    /**
     * Creates a base version, saves entities to version, and returns result.
     *
     * @param project  The project identifier to relate to version and entities.
     * @param entities The entities to save to project version.
     * @return ProjectEntities containing all saved entities.
     * @throws SafaError Throws error is something occurs while creating artifacts or traces.
     */
    public ProjectVersionErrors createNewProjectWithVersion(Project project,
                                                            ProjectAppEntity entities) throws SafaError {
        ProjectVersionErrors projectEntities;

        this.saveProjectWithCurrentUserAsOwner(project);
        ProjectVersion projectVersion = this.createBaseProjectVersion(project);
        projectEntities = entityVersionService.setProjectEntitiesAtVersion(
            projectVersion,
            entities.getArtifacts(),
            entities.getTraces());
        return projectEntities;
    }

    public void saveProjectWithCurrentUserAsOwner(Project project) {
        this.projectRepository.save(project);
        this.setCurrentUserAsOwner(project);
    }

    public ProjectVersion createBaseProjectVersion(Project project) {
        ProjectVersion projectVersion = new ProjectVersion(project, 1, 1, 1);
        this.projectVersionRepository.save(projectVersion);
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
