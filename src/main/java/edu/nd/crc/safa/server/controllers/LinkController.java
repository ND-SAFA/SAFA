package edu.nd.crc.safa.server.controllers;

import java.util.List;

import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.db.entities.sql.TraceLink;
import edu.nd.crc.safa.db.repositories.ProjectRepository;
import edu.nd.crc.safa.db.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.db.repositories.TraceLinkRepository;
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
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class LinkController extends BaseController {

    TraceLinkRepository traceLinkRepository;
    FlatFileService flatFileService;

    @Autowired
    public LinkController(ProjectRepository projectRepository,
                          ProjectVersionRepository projectVersionRepository,
                          TraceLinkRepository traceLinkRepository,
                          TraceLinkService traceLinkService,
                          FlatFileService flatFileService) {
        super(projectRepository, projectVersionRepository);
        this.traceLinkRepository = traceLinkRepository;
        this.flatFileService = flatFileService;
    }

    @GetMapping("projects/{projectId}/links/")
    public ServerResponse getLink(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        List<TraceLink> projectLinks = traceLinkRepository.findByProject(project);
        return new ServerResponse(projectLinks);
    }

    @PostMapping("projects/{projectId}/link/")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void updateLink(@PathVariable String projectId,
                           @RequestBody TraceLink traceLink) throws ServerError {
        // TODO: Validate that user has access to trace link
        this.traceLinkRepository.save(traceLink);
    }
}
