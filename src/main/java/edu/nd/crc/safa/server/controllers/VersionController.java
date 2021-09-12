package edu.nd.crc.safa.server.controllers;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.importer.Puller;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.db.repositories.ProjectRepository;
import edu.nd.crc.safa.server.db.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.responses.ServerError;
import edu.nd.crc.safa.server.responses.ServerResponse;
import edu.nd.crc.safa.server.services.ProjectService;
import edu.nd.crc.safa.server.services.VersionService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@CrossOrigin
@RestController
public class VersionController extends BaseController {

    Puller mPuller;
    VersionService versionService;
    ProjectService projectService;

    @Autowired
    public VersionController(ProjectRepository projectRepository,
                             ProjectVersionRepository projectVersionRepository,
                             Puller mPuller,
                             VersionService versionService,
                             ProjectService projectService) {
        super(projectRepository, projectVersionRepository);
        this.mPuller = mPuller;
        this.versionService = versionService;
        this.projectService = projectService;
    }

    @GetMapping("projects/{projectId}/versions")
    public ServerResponse versions(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        return new ServerResponse(versionService.getProjectVersions(project));
    }

    @GetMapping("projects/{projectId}/versions/current")
    public ServerResponse getCurrentVersion(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        return new ServerResponse(versionService.getCurrentVersion(project));
    }

    @PostMapping("projects/{projectId}/versions/major")
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse createNewMajorVersion(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        ProjectVersion nextVersion = versionService.createNewMajorVersion(project);
        return new ServerResponse(nextVersion);
    }

    @PostMapping("projects/{projectId}/versions/minor")
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse createNewMinorVersion(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        ProjectVersion nextVersion = versionService.createNewMinorVersion(project);
        return new ServerResponse(nextVersion);
    }

    @PostMapping("projects/{projectId}/versions/revision")
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse createNewRevisionVersion(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        ProjectVersion nextVersion = versionService.createNextRevision(project);
        return new ServerResponse(nextVersion);
    }

    @DeleteMapping("projects/versions/{versionId}")
    public ServerResponse deleteVersion(@PathVariable UUID versionId) throws ServerError {
        Optional<ProjectVersion> versionQuery = this.projectVersionRepository.findById(versionId);
        if (versionQuery.isPresent()) {
            this.projectVersionRepository.delete(versionQuery.get());
            return new ServerResponse("Project version deleted successfully");
        } else {
            throw new ServerError("Could not find version with id:" + versionId);
        }
    }

    @GetMapping("projects/versions/{versionId}")
    public ServerResponse getProjectById(@PathVariable UUID versionId) throws ServerError {
        Optional<ProjectVersion> versionQuery = this.projectVersionRepository.findById(versionId);
        if (versionQuery.isPresent()) {
            return new ServerResponse(this.projectService.createApplicationEntity(versionQuery.get()));
        } else {
            throw new ServerError("Could not find version with id: " + versionId);
        }
    }
}
