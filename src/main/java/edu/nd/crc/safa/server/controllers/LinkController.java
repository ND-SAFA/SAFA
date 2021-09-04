package edu.nd.crc.safa.server.controllers;

import java.util.List;

import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.db.entities.sql.TraceLink;
import edu.nd.crc.safa.db.repositories.sql.ProjectRepository;
import edu.nd.crc.safa.db.repositories.sql.ProjectVersionRepository;
import edu.nd.crc.safa.db.repositories.sql.TraceLinkRepository;
import edu.nd.crc.safa.server.responses.ServerError;
import edu.nd.crc.safa.server.responses.ServerResponse;
import edu.nd.crc.safa.server.services.FlatFileService;
import edu.nd.crc.safa.server.services.TraceLinkService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class LinkController extends BaseController {

    TraceLinkRepository traceLinkRepository;
    TraceLinkService traceLinkService;
    FlatFileService flatFileService;

    @Autowired
    public LinkController(ProjectRepository projectRepository,
                          ProjectVersionRepository projectVersionRepository,
                          TraceLinkRepository traceLinkRepository,
                          TraceLinkService traceLinkService,
                          FlatFileService flatFileService) {
        super(projectRepository, projectVersionRepository);
        this.traceLinkRepository = traceLinkRepository;
        this.traceLinkService = traceLinkService;
        this.flatFileService = flatFileService;
    }

    @GetMapping("projects/{projectId}/link/")
    public ServerResponse getLink(@PathVariable String projectId,
                                  @RequestParam("source") String source,
                                  @RequestParam("target") String target) throws ServerError {
        Project project = getProject(projectId);
        return new ServerResponse(traceLinkService.getLink(project, source, target));
    }

    @PostMapping("projects/{projectId}/link/")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void updateLink(@PathVariable String projectId,
                           @RequestBody TraceLink traceLink) throws ServerError {
        // TODO: Validate that user has access to trace link
        this.traceLinkRepository.save(traceLink);
    }

    @GetMapping("projects/{projectId}/artifact/{source}/links")
    public ServerResponse getLinksWithSource(@PathVariable String projectId,
                                             @PathVariable String sourceName,
                                             @RequestParam(value = "target", required = false) String target,
                                             @RequestParam(name = "minScore", required = false, defaultValue = "0.0")
                                                 Double minScore) throws ServerError {
        Project project = getProject(projectId);
        List<TraceLink> traceLinks = traceLinkService.getArtifactLinks(project, sourceName, target, minScore);
        return new ServerResponse(traceLinks);
    }

    @GetMapping("projects/{projectId}/linktypes/")
    public ServerResponse getLinkTypes(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        return new ServerResponse(traceLinkService.getLinkTypes(project));
    }

    @GetMapping("projects/{projectId}/generate/")
    public void generateLinks(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        ProjectVersion projectVersion = getCurrentVersion(project);
        flatFileService.generateLinks(project, projectVersion); //TODO: return any error logs
    }
}
