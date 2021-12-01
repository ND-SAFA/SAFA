package edu.nd.crc.safa.server.services;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.api.ProjectEntities;
import edu.nd.crc.safa.server.entities.api.ServerError;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectMembership;
import edu.nd.crc.safa.server.entities.db.ProjectRole;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.SafaUser;
import edu.nd.crc.safa.server.repositories.ProjectMemberRepository;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.repositories.SafaUserRepository;
import edu.nd.crc.safa.utilities.OSHelper;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Responsible for updating, deleting, and retrieving projects.
 */
@Service
public class ProjectService {

    ProjectRepository projectRepository;
    ProjectVersionRepository projectVersionRepository;
    ProjectMemberRepository projectMemberRepository;
    SafaUserRepository safaUserRepository;

    TraceLinkService traceLinkService;
    ProjectRetrievalService projectRetrievalService;
    ParserErrorService parserErrorService;
    ArtifactVersionService artifactVersionService;
    WarningService warningService;

    @Autowired
    public ProjectService(ProjectRepository projectRepository,
                          ProjectVersionRepository projectVersionRepository,
                          ProjectMemberRepository projectMemberRepository,
                          SafaUserRepository safaUserRepository,
                          ParserErrorService parserErrorService,
                          ArtifactVersionService artifactVersionService,
                          TraceLinkService traceLinkService,
                          WarningService warningService,
                          ProjectRetrievalService projectRetrievalService) {
        this.projectRepository = projectRepository;
        this.projectVersionRepository = projectVersionRepository;
        this.projectMemberRepository = projectMemberRepository;
        this.safaUserRepository = safaUserRepository;
        this.parserErrorService = parserErrorService;
        this.artifactVersionService = artifactVersionService;
        this.traceLinkService = traceLinkService;
        this.warningService = warningService;
        this.projectRetrievalService = projectRetrievalService;
    }

    /**
     * Saves given artifacts and traces to given version. Note, if given version
     * already contains records of given entities, they are replaced.
     *
     * @param projectVersion The version to store the entities to.
     * @param artifacts      The artifacts to store to version.
     * @param traces         The traces to store to version.
     * @return ProjectEntities representing current state of project version after modification.
     * @throws ServerError Throws error is a problem occurs while saving artifacts or traces.
     */
    @Transactional
    public ProjectEntities saveProjectEntitiesToVersion(ProjectVersion projectVersion,
                                                        @NotNull List<ArtifactAppEntity> artifacts,
                                                        @NotNull List<TraceAppEntity> traces) throws ServerError {

        artifactVersionService.setArtifactsAtVersion(projectVersion, artifacts);
        traceLinkService.createTraceLinks(projectVersion, traces);
        return projectRetrievalService.retrieveAndCreateProjectResponse(projectVersion);
    }

    /**
     * Deletes given project and all related entities through cascade property.
     *
     * @param project The project to delete.
     * @throws ServerError Throws error if error occurs while deleting flat files.
     */
    public void deleteProject(Project project) throws ServerError {
        this.projectRepository.delete(project);
        OSHelper.deletePath(ProjectPaths.getPathToStorage(project));
    }

    /**
     * Returns the projects owned by user or projects in which they are members.
     *
     * @param user The user whose projects are being retrieved.
     * @return List of projects where given user has access to.
     */
    public List<Project> getUserProjects(SafaUser user) {
        List<Project> ownerProjects = this.projectRepository.findByOwner(user);
        List<Project> sharedProjects =
            this.projectMemberRepository
                .findByMember(user)
                .stream()
                .map(ProjectMembership::getProject)
                .collect(Collectors.toList());
        ownerProjects.addAll(sharedProjects);
        return ownerProjects;
    }

    public ProjectEntities updateProjectAtVersion(Project project,
                                                  ProjectVersion projectVersion,
                                                  ProjectAppEntity payload) throws ServerError {
        ProjectEntities response;
        Project persistentProject = this.projectRepository.findByProjectId(project.getProjectId());
        persistentProject.setName(project.getName());
        persistentProject.setDescription(project.getDescription());
        //TODO: Update owner here.
        this.projectRepository.save(persistentProject);
        //TODO: Update traces
        if (projectVersion == null) {
            if ((payload.artifacts != null
                && payload.artifacts.size() > 0)) {
                throw new ServerError("Cannot update artifacts because project version not defined");
            }
            response = new ProjectEntities(payload, null, null, null);
        } else if (!projectVersion.hasValidId()) {
            throw new ServerError("Invalid Project version: must have a valid ID.");
        } else if (!projectVersion.hasValidVersion()) {
            throw new ServerError("Invalid Project version: must contain positive major, minor, and revision "
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
        ProjectAppEntity payload) throws ServerError {
        ProjectEntities entityCreationResponse;
        if (projectVersion != null
            && projectVersion.hasValidVersion()
            && projectVersion.hasValidId()) {
            throw new ServerError("Invalid ProjectVersion: cannot be defined when creating a new project.");
        }
        this.projectRepository.save(project);
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

    public void addMemberToProject(UUID projectId, String memberEmail, ProjectRole role) {
        Project project = this.projectRepository.findByProjectId(projectId);
        SafaUser member = this.safaUserRepository.findByEmail(memberEmail);
        ProjectMembership projectMembership = new ProjectMembership(project, member, role);
        this.projectMemberRepository.save(projectMembership);
    }
}
