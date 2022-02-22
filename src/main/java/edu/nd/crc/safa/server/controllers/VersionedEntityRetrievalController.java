package edu.nd.crc.safa.server.controllers;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.ProjectEntities;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.services.ProjectRetrievalService;
import edu.nd.crc.safa.server.services.VersionService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

/**
 * Provides endpoints for retrieving, creating, and deleting project versions.
 */
@RestController
public class VersionedEntityRetrievalController extends BaseController {

    private final VersionService versionService;
    private final ProjectRetrievalService projectRetrievalService;

    @Autowired
    public VersionedEntityRetrievalController(ProjectRepository projectRepository,
                                              ProjectVersionRepository projectVersionRepository,
                                              ResourceBuilder resourceBuilder,
                                              VersionService versionService,
                                              ProjectRetrievalService projectRetrievalService) {
        super(projectRepository, projectVersionRepository, resourceBuilder);
        this.versionService = versionService;
        this.projectRetrievalService = projectRetrievalService;
    }

    /**
     * Returns a project and associated artifacts at version associated with given id.
     *
     * @param versionId UUID of version whose artifacts and trace links are retrieved.
     * @return ProjectCreationResponse containing artifacts, traces, and warnings of project at version specified.
     * @throws SafaError Throws error if no version is associated with given id.
     */
    @GetMapping(AppRoutes.Projects.getProjectInVersion)
    public ProjectEntities getProjectInVersion(@PathVariable UUID versionId) throws SafaError {
        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withViewVersion();
        ProjectEntities response = this.projectRetrievalService
            .retrieveAndCreateProjectResponse(projectVersion);
        return response;
    }

    /**
     * Returns the current list of artifacts in the specified project version.
     *
     * @param versionId The UUID of the project version whose artifacts are being retrieved.
     * @return List of artifact app entities.
     * @throws SafaError Throws error is user does not have read permission on the project.
     */
    @GetMapping(AppRoutes.Projects.getArtifactsInVersion)
    public List<ArtifactAppEntity> getArtifactsInVersion(@PathVariable UUID versionId) throws SafaError {
        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withViewVersion();
        return this.projectRetrievalService.getArtifactInProjectVersion(projectVersion);
    }

    /**
     * Returns the current list of traces in the specified project version.
     *
     * @param versionId The UUID of the version whose traces are returned
     * @return List of trace app entities existing in specified version.
     * @throws SafaError Throws error is authorized user does not have read permission on the project.
     */
    @GetMapping(AppRoutes.Projects.getTracesInVersion)
    public List<TraceAppEntity> getTracesInVersion(@PathVariable UUID versionId) throws SafaError {
        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withViewVersion();
        List<TraceAppEntity> traces = this.projectRetrievalService.getTracesInProjectVersion(projectVersion);
        return traces;
    }
}
