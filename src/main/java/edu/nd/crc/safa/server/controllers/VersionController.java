package edu.nd.crc.safa.server.controllers;

import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.db.repositories.ProjectRepository;
import edu.nd.crc.safa.db.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.importer.Puller;
import edu.nd.crc.safa.server.responses.ServerError;
import edu.nd.crc.safa.server.responses.ServerResponse;
import edu.nd.crc.safa.server.services.VersionService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
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

    @GetMapping("projects/{projectId}/versions/")
    public ServerResponse versions(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        return new ServerResponse(versionService.getProjectVersions(project));
    }
}
