package edu.nd.crc.safa.server.services;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.db.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.db.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.server.db.entities.app.TraceApplicationEntity;
import edu.nd.crc.safa.server.db.entities.sql.ArtifactBody;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.db.entities.sql.TraceLink;
import edu.nd.crc.safa.server.db.repositories.ArtifactBodyRepository;
import edu.nd.crc.safa.server.db.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.db.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.server.db.repositories.ParserErrorRepository;
import edu.nd.crc.safa.server.db.repositories.ProjectRepository;
import edu.nd.crc.safa.server.db.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.db.repositories.TraceLinkRepository;
import edu.nd.crc.safa.server.messages.ProjectCreationResponse;
import edu.nd.crc.safa.server.messages.ProjectErrors;
import edu.nd.crc.safa.server.messages.ServerError;
import edu.nd.crc.safa.utilities.OSHelper;
import edu.nd.crc.safa.warnings.RuleName;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class ProjectService {
    /**
     * Responsible for all providing an API for performing the
     * business logic involved in ProjectsController.
     */
    ProjectRepository projectRepository;
    ProjectVersionRepository projectVersionRepository;
    ArtifactRepository artifactRepository;
    ArtifactTypeRepository artifactTypeRepository;
    ArtifactBodyRepository artifactBodyRepository;
    TraceLinkRepository traceLinkRepository;
    ParserErrorRepository parserErrorRepository;
    ParserErrorService parserErrorService;
    ArtifactVersionService artifactVersionService;
    TraceLinkService traceLinkService;
    WarningService warningService;

    @Autowired
    public ProjectService(ProjectRepository projectRepository,
                          ProjectVersionRepository projectVersionRepository,
                          ArtifactRepository artifactRepository,
                          ArtifactTypeRepository artifactTypeRepository,
                          ArtifactBodyRepository artifactBodyRepository,
                          TraceLinkRepository traceLinkRepository,
                          ParserErrorRepository parserErrorRepository,
                          ParserErrorService parserErrorService,
                          ArtifactVersionService artifactVersionService,
                          TraceLinkService traceLinkService,
                          WarningService warningService) {
        this.projectRepository = projectRepository;
        this.projectVersionRepository = projectVersionRepository;
        this.artifactRepository = artifactRepository;
        this.artifactTypeRepository = artifactTypeRepository;
        this.artifactBodyRepository = artifactBodyRepository;
        this.traceLinkRepository = traceLinkRepository;
        this.parserErrorRepository = parserErrorRepository;
        this.parserErrorService = parserErrorService;
        this.artifactVersionService = artifactVersionService;
        this.traceLinkService = traceLinkService;
        this.warningService = warningService;
    }

    @Transactional
    public ProjectCreationResponse saveProjectAppEntity(ProjectVersion projectVersion,
                                                        ProjectAppEntity appEntity) throws ServerError {

        if (appEntity.artifacts != null) {
            artifactVersionService.setArtifactsAtVersion(projectVersion, appEntity.getArtifacts());
        }

        if (appEntity.traces != null) {
            traceLinkService.createTraceLinks(projectVersion, appEntity.getTraces());
        }

        return this.retrieveAndCreateProjectResponse(projectVersion);
    }

    @Transactional
    public ProjectCreationResponse updateProject(ProjectVersion projectVersion,
                                                 ProjectAppEntity appEntity) throws ServerError {

        artifactVersionService.setArtifactsAtVersion(projectVersion, appEntity.getArtifacts());

        //TODO: Update trace links
        Map<String, List<RuleName>> projectWarnings = warningService.findViolationsInArtifactTree(projectVersion);
        ProjectErrors projectErrors = this.parserErrorService.collectionProjectErrors(projectVersion);
        return new ProjectCreationResponse(appEntity, projectVersion, projectErrors, projectWarnings); // TODO:
        // Actually retrieve new
    }

    public ProjectCreationResponse retrieveAndCreateProjectResponse(ProjectVersion projectVersion) {
        ProjectAppEntity projectAppEntity = createApplicationEntity(projectVersion);
        ProjectErrors projectErrors = this.parserErrorService.collectionProjectErrors(projectVersion);
        Map<String, List<RuleName>> projectWarnings = this.warningService.findViolationsInArtifactTree(projectVersion);
        return new ProjectCreationResponse(projectAppEntity, projectVersion, projectErrors, projectWarnings);
    }

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
        List<TraceApplicationEntity> traces =
            traceLinks
                .stream()
                .map(TraceApplicationEntity::new)
                .collect(Collectors.toList());
        return new ProjectAppEntity(projectVersion, artifacts, traces);
    }

    public void deleteProject(Project project) throws ServerError {
        this.projectRepository.delete(project);
        OSHelper.deletePath(ProjectPaths.getPathToStorage(project));
    }
}
