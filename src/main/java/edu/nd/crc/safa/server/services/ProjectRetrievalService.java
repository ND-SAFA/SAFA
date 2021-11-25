package edu.nd.crc.safa.server.services;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.server.entities.api.ProjectEntities;
import edu.nd.crc.safa.server.entities.api.ProjectParsingErrors;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.ArtifactBody;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceLink;
import edu.nd.crc.safa.server.repositories.TraceLinkRepository;
import edu.nd.crc.safa.warnings.RuleName;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Responsible for all providing an API to retrieve and collect project related enities including:
 * 1. ProjectCreationResponse
 * 2. ProjectAppEntity
 */
@Service
public class ProjectRetrievalService {

    TraceLinkRepository traceLinkRepository;
    ArtifactVersionService artifactVersionService;
    ParserErrorService parserErrorService;
    WarningService warningService;

    @Autowired
    public ProjectRetrievalService(TraceLinkRepository traceLinkRepository,
                                   ParserErrorService parserErrorService,
                                   ArtifactVersionService artifactVersionService,
                                   WarningService warningService) {
        this.traceLinkRepository = traceLinkRepository;
        this.parserErrorService = parserErrorService;
        this.artifactVersionService = artifactVersionService;
        this.warningService = warningService;
    }

    /**
     * Finds project, artifact, traces, errors, and warnings related with given project version.
     *
     * @param projectVersion Version whose artifacts are used to generate warnings and error
     * @return ProjectCreationResponse containing all relevant project entities
     */
    public ProjectEntities retrieveAndCreateProjectResponse(ProjectVersion projectVersion) {
        ProjectAppEntity projectAppEntity = createApplicationEntity(projectVersion);
        ProjectParsingErrors projectParsingErrors = this.parserErrorService.collectionProjectErrors(projectVersion);
        Map<String, List<RuleName>> projectWarnings = this.warningService.findViolationsInArtifactTree(projectVersion);
        return new ProjectEntities(projectAppEntity, projectVersion, projectParsingErrors, projectWarnings);
    }

    /**
     * Finds artifacts and trace links existing in given project version.
     *
     * @param projectVersion The point in the project whose entities are being retrieved.
     * @return ProjectAppEntity Entity containing project name, description, artifacts, and traces.
     */
    public ProjectAppEntity createApplicationEntity(ProjectVersion projectVersion) {
        Project project = projectVersion.getProject();
        List<ArtifactBody> artifactBodies = artifactVersionService
            .getArtifactBodiesAtVersion(projectVersion);

        List<ArtifactAppEntity> artifacts =
            artifactBodies
                .stream()
                .map(ArtifactAppEntity::new)
                .collect(Collectors.toList());
        List<TraceLink> traceLinks = this.traceLinkRepository
            .getUnDeclinedLinks(project);
        List<TraceAppEntity> traces =
            traceLinks
                .stream()
                .map(TraceAppEntity::new)
                .collect(Collectors.toList());
        return new ProjectAppEntity(projectVersion, artifacts, traces);
    }
}
