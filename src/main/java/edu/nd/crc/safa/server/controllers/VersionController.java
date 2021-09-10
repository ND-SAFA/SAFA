package edu.nd.crc.safa.server.controllers;

import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.db.repositories.ProjectRepository;
import edu.nd.crc.safa.db.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.importer.Puller;
import edu.nd.crc.safa.server.responses.ServerError;
import edu.nd.crc.safa.server.responses.ServerResponse;
import edu.nd.crc.safa.server.services.VersionService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class VersionController extends BaseController {

    Puller mPuller;
    VersionService versionService;

    @Autowired
    public VersionController(ProjectRepository projectRepository,
                             ProjectVersionRepository projectVersionRepository,
                             Puller mPuller,
                             VersionService versionService) {
        super(projectRepository, projectVersionRepository);
        this.mPuller = mPuller;
        this.versionService = versionService;
    }

    @GetMapping("projects/{projectId}/versions")
    public ServerResponse versions(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        return new ServerResponse(versionService.getProjectVersions(project));
    }

    @PostMapping("projects/{projectId}/versions/revisions")
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse createNewRevisionVersion(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        ProjectVersion nextVersion = versionService.createNextRevision(project);
        return new ServerResponse(nextVersion);
    }

    @PostMapping("projects/{projectId}/versions/minor")
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse createNewMinorVersion(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        ProjectVersion nextVersion = versionService.createNewMinorVersion(project);
        return new ServerResponse(nextVersion);
    }

    @PostMapping("projects/{projectId}/versions/major")
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse createNewMajorVersion(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        ProjectVersion nextVersion = versionService.createNewMajorVersion(project);
        return new ServerResponse(nextVersion);
    }
}
