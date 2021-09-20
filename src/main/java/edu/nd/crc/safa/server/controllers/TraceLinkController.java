package edu.nd.crc.safa.server.controllers;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.server.db.entities.app.TraceApplicationEntity;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.TraceLink;
import edu.nd.crc.safa.server.db.repositories.ProjectRepository;
import edu.nd.crc.safa.server.db.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.db.repositories.TraceLinkRepository;
import edu.nd.crc.safa.server.responses.ServerResponse;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@CrossOrigin
@RestController
public class TraceLinkController extends BaseController {

    TraceLinkRepository traceLinkRepository;

    @Autowired
    public TraceLinkController(ProjectRepository projectRepository,
                               ProjectVersionRepository projectVersionRepository,
                               TraceLinkRepository traceLinkRepository) {
        super(projectRepository, projectVersionRepository);
        this.traceLinkRepository = traceLinkRepository;
    }

    @GetMapping("/projects/{projectId}/links/generated")
    public ServerResponse getGeneratedLinks(@PathVariable UUID projectId) {
        Project project = this.projectRepository.findByProjectId(projectId);
        List<TraceLink> projectLinks = this.traceLinkRepository.getProjectGeneratedLinks(project);
        return new ServerResponse(TraceApplicationEntity.createEntities(projectLinks));
    }
}
