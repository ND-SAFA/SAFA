package edu.nd.crc.safa.server.controllers;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.importer.tracegenerator.TraceLinkGenerator;
import edu.nd.crc.safa.server.entities.api.ServerError;
import edu.nd.crc.safa.server.entities.api.ServerResponse;
import edu.nd.crc.safa.server.entities.api.TraceLinkGenerationRequest;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.TraceLink;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.repositories.TraceLinkRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/**
 * Responsible for generating trace links between artifact types and
 * retrieving them.
 */
@RestController
public class GeneratedLinkController extends BaseController {

    TraceLinkRepository traceLinkRepository;
    TraceLinkGenerator traceLinkGenerator;

    @Autowired
    public GeneratedLinkController(ProjectRepository projectRepository,
                                   ProjectVersionRepository projectVersionRepository,
                                   ResourceBuilder resourceBuilder,
                                   TraceLinkRepository traceLinkRepository,
                                   TraceLinkGenerator traceLinkGenerator) {
        super(projectRepository, projectVersionRepository, resourceBuilder);
        this.traceLinkRepository = traceLinkRepository;
        this.traceLinkGenerator = traceLinkGenerator;
    }

    @GetMapping(value = AppRoutes.Projects.getGeneratedLinks)
    public ServerResponse getGeneratedLinks(@PathVariable UUID projectId) throws ServerError {
        Project project = this.resourceBuilder.fetchProject(projectId).withViewProject();
        List<TraceLink> projectLinks = this.traceLinkRepository.getGeneratedLinks(project);
        return new ServerResponse(TraceAppEntity.createEntities(projectLinks));
    }

    @PostMapping(value = AppRoutes.Projects.generateLinks)
    public ServerResponse generateTraceLinks(@RequestBody TraceLinkGenerationRequest traceLinkGenerationRequest) {
        List<ArtifactAppEntity> sourceArtifacts = traceLinkGenerationRequest.getSourceArtifacts();
        List<ArtifactAppEntity> targetArtifacts = traceLinkGenerationRequest.getTargetArtifacts();
        return new ServerResponse(traceLinkGenerator.generateLinksBetweenArtifactAppEntities(sourceArtifacts,
            targetArtifacts));
    }
}
