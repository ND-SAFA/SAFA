package edu.nd.crc.safa.server.services;

import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.authentication.SafaUserService;
import edu.nd.crc.safa.server.entities.api.ProjectEntities;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectMembership;
import edu.nd.crc.safa.server.entities.db.ProjectRole;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.SafaUser;
import edu.nd.crc.safa.server.repositories.ProjectMembershipRepository;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.repositories.SafaUserRepository;
import edu.nd.crc.safa.utilities.OSHelper;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.PathVariable;

/**
 * Responsible for updating, deleting, and retrieving projects.
 */
@Service
public class ProjectService {

    ProjectRepository projectRepository;
    ProjectVersionRepository projectVersionRepository;
    ProjectMembershipRepository projectMembershipRepository;
    SafaUserRepository safaUserRepository;

    SafaUserService safaUserService;
    TraceLinkService traceLinkService;
    ProjectRetrievalService projectRetrievalService;
    ParserErrorService parserErrorService;
    EntityVersionService entityVersionService;
    WarningService warningService;
    PermissionService permissionService;

    @Autowired
    public ProjectService(ProjectRepository projectRepository,
                          ProjectVersionRepository projectVersionRepository,
                          ProjectMembershipRepository projectMembershipRepository,
                          SafaUserRepository safaUserRepository,
                          SafaUserService safaUserService,
                          ParserErrorService parserErrorService,
                          EntityVersionService entityVersionService,
                          TraceLinkService traceLinkService,
                          WarningService warningService,
                          ProjectRetrievalService projectRetrievalService,
                          PermissionService permissionService) {
        this.projectRepository = projectRepository;
        this.projectVersionRepository = projectVersionRepository;
        this.projectMembershipRepository = projectMembershipRepository;
        this.safaUserRepository = safaUserRepository;
        this.safaUserService = safaUserService;
        this.parserErrorService = parserErrorService;
        this.entityVersionService = entityVersionService;
        this.traceLinkService = traceLinkService;
        this.warningService = warningService;
        this.projectRetrievalService = projectRetrievalService;
        this.permissionService = permissionService;
    }

    /**
     * Saves given artifacts and traces to given version. Note, if given version
     * already contains records of given entities, they are replaced.
     *
     * @param projectVersion The version to store the entities to.
     * @param artifacts      The artifacts to store to version.
     * @param traces         The traces to store to version.
     * @return ProjectEntities representing current state of project version after modification.
     * @throws SafaError Throws error is a problem occurs while saving artifacts or traces.
     */
    @Transactional
    public ProjectEntities saveProjectEntitiesToVersion(ProjectVersion projectVersion,
                                                        @NotNull List<ArtifactAppEntity> artifacts,
                                                        @NotNull List<TraceAppEntity> traces) throws SafaError {

        entityVersionService.setArtifactsAtVersion(projectVersion, artifacts);
        entityVersionService.setTracesAtVersion(projectVersion, traces);
        return projectRetrievalService.retrieveAndCreateProjectResponse(projectVersion);
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
    public List<Project> getCurrentUserProjects() {
        SafaUser user = this.safaUserService.getCurrentUser();
        return this.projectMembershipRepository
            .findByMember(user)
            .stream()
            .map(ProjectMembership::getProject)
            .collect(Collectors.toList());
    }

    public ProjectEntities updateProjectAtVersion(Project project,
                                                  ProjectVersion projectVersion,
                                                  ProjectAppEntity payload) throws SafaError {
        ProjectEntities response;
        Project persistentProject = this.projectRepository.findByProjectId(project.getProjectId());
        persistentProject.setName(project.getName());
        persistentProject.setDescription(project.getDescription());
        this.projectRepository.save(persistentProject);
        //TODO: Update traces
        if (projectVersion == null) {
            if ((payload.artifacts != null
                && payload.artifacts.size() > 0)) {
                throw new SafaError("Cannot update artifacts because project version not defined");
            }
            response = new ProjectEntities(payload, null, null, null);
        } else if (!projectVersion.hasValidId()) {
            throw new SafaError("Invalid Project version: must have a valid ID.");
        } else if (!projectVersion.hasValidVersion()) {
            throw new SafaError("Invalid Project version: must contain positive major, minor, and revision "
                + "numbers.");
        } else {
            projectVersion.setProject(project);
            this.projectVersionRepository.save(projectVersion);
            response = this.saveProjectEntitiesToVersion(projectVersion,
                payload.getArtifacts(),
                payload.getTraces());
        }
        return response;
    }

    public ProjectEntities createNewProjectWithVersion(
        Project project,
        ProjectVersion projectVersion,
        ProjectAppEntity payload) throws SafaError {
        ProjectEntities entityCreationResponse;
        if (projectVersion != null
            && projectVersion.hasValidVersion()
            && projectVersion.hasValidId()) {
            throw new SafaError("Invalid ProjectVersion: cannot be defined when creating a new project.");
        }
        this.projectRepository.save(project);
        this.setCurrentUserAsOwner(project);
        projectVersion = this.createBaseProjectVersion(project);
        entityCreationResponse = this.saveProjectEntitiesToVersion(
            projectVersion,
            payload.getArtifacts(),
            payload.getTraces());
        return entityCreationResponse;
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
            if (newMemberRole.compareTo(currentUserMembershipQuery.get().getRole()) >= 0) {
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
     */
    public void deleteProjectMemberById(@PathVariable UUID projectMembershipId) throws SafaError {
        Optional<ProjectMembership> projectMembershipQuery =
            this.projectMembershipRepository.findById(projectMembershipId);
        if (projectMembershipQuery.isPresent()) {
            this.projectMembershipRepository.delete(projectMembershipQuery.get());
        }
    }
}
