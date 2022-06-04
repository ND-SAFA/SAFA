package edu.nd.crc.safa.server.controllers;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.importer.tracegenerator.TraceLinkGenerator;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.api.TraceLinkGenerationRequest;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceType;
import edu.nd.crc.safa.server.services.retrieval.AppEntityRetrievalService;

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

    private final TraceLinkGenerator traceLinkGenerator;
    private final AppEntityRetrievalService appEntityRetrievalService;

    @Autowired
    public GeneratedLinkController(ResourceBuilder resourceBuilder,
                                   AppEntityRetrievalService appEntityRetrievalService,
                                   TraceLinkGenerator traceLinkGenerator) {
        super(resourceBuilder);
        this.appEntityRetrievalService = appEntityRetrievalService;
        this.traceLinkGenerator = traceLinkGenerator;
    }

    /**
     * Returns generated links in project version.
     *
     * @param versionId The UUID of project version to retrieve from.
     * @return List of trace app entities representing generated links in project version.
     * @throws SafaError If user does not have permissions to access this project.
     */
    @GetMapping(value = AppRoutes.Projects.Links.getGeneratedLinksInProjectVersion)
    public List<TraceAppEntity> getGeneratedLinks(@PathVariable UUID versionId) throws SafaError {
        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withViewVersion();
        List<TraceAppEntity> traces = this.appEntityRetrievalService
            .retrieveTracesInProjectVersion(projectVersion);
        return this.appEntityRetrievalService
            .retrieveTracesInProjectVersion(projectVersion)
            .stream()
            .filter(t -> t.traceType.equals(TraceType.GENERATED))
            .collect(Collectors.toList());
    }

    /**
     * Generates links between source and target artifacts.
     *
     * @param traceLinkGenerationRequest Request containing source and target artifacts.
     * @return Returns list of trace app entities
     */
    @PostMapping(value = AppRoutes.Projects.Links.generateLinks)
    public List<TraceAppEntity> generateTraceLinks(@RequestBody TraceLinkGenerationRequest traceLinkGenerationRequest) {
        List<ArtifactAppEntity> sourceArtifacts = traceLinkGenerationRequest.getSourceArtifacts();
        List<ArtifactAppEntity> targetArtifacts = traceLinkGenerationRequest.getTargetArtifacts();
        return traceLinkGenerator.generateLinksBetweenArtifactAppEntities(sourceArtifacts, targetArtifacts);
    }
}
