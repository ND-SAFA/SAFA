package edu.nd.crc.safa.server.services;

import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.api.ProjectCreationResponse;
import edu.nd.crc.safa.server.entities.api.ProjectErrors;
import edu.nd.crc.safa.server.entities.api.ServerError;
import edu.nd.crc.safa.server.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.utilities.OSHelper;
import edu.nd.crc.safa.warnings.RuleName;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Responsible for all providing an API for performing the
 * business logic involved in ProjectsController.
 */
@Service
public class ProjectService {

    ProjectRepository projectRepository;

    TraceLinkService traceLinkService;
    ProjectRetrievalService projectRetrievalService;
    ParserErrorService parserErrorService;
    ArtifactVersionService artifactVersionService;
    WarningService warningService;

    @Autowired
    public ProjectService(ProjectRepository projectRepository,
                          ParserErrorService parserErrorService,
                          ArtifactVersionService artifactVersionService,
                          TraceLinkService traceLinkService,
                          WarningService warningService,
                          ProjectRetrievalService projectRetrievalService) {
        this.projectRepository = projectRepository;
        this.parserErrorService = parserErrorService;
        this.artifactVersionService = artifactVersionService;
        this.traceLinkService = traceLinkService;
        this.warningService = warningService;
        this.projectRetrievalService = projectRetrievalService;
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

        return projectRetrievalService.retrieveAndCreateProjectResponse(projectVersion);
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

    public void deleteProject(Project project) throws ServerError {
        this.projectRepository.delete(project);
        OSHelper.deletePath(ProjectPaths.getPathToStorage(project));
    }
}
