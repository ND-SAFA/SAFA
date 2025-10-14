package edu.nd.crc.safa.features.projects.controllers;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/**
 * Provides endpoints for retrieving, creating, and deleting project versions.
 */
@RestController
public class RetrievalController extends BaseController {

    @Autowired
    public RetrievalController(ResourceBuilder resourceBuilder,
                               ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
    }


    /**
     * Returns a project and associated artifacts at version associated with given id.
     *
     * @param versionId UUID of version whose artifacts and trace links are retrieved.
     * @return ProjectCreationResponse containing artifacts, traces, and warnings of project at version specified.
     * @throws SafaError Throws error if no version is associated with given id.
     */
    @GetMapping(AppRoutes.Retrieval.GET_PROJECT_IN_VERSION)
    public ProjectAppEntity getProjectInVersion(@PathVariable UUID versionId) throws SafaError {
        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
        ProjectVersion projectVersion = getResourceBuilder().fetchVersion(versionId)
                .withPermission(ProjectPermission.VIEW, user).get();
        return getServiceProvider()
            .getProjectRetrievalService()
            .getProjectAppEntity(projectVersion);
    }

    /**
     * Returns the current list of artifacts in the specified project version.
     *
     * @param versionId The UUID of the project version whose artifacts are being retrieved.
     * @return List of artifact app entities.
     * @throws SafaError Throws error is user does not have read permission on the project.
     */
    @GetMapping(AppRoutes.Retrieval.GET_ARTIFACTS_IN_VERSION)
    public List<ArtifactAppEntity> getArtifactsInProjectVersion(@PathVariable UUID versionId) throws SafaError {
        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
        ProjectVersion projectVersion = getResourceBuilder().fetchVersion(versionId)
                .withPermission(ProjectPermission.VIEW, user).get();
        return getServiceProvider().getArtifactService().getAppEntities(projectVersion, user);
    }

    /**
     * Returns list of artifacts corresponding with given artifact IDs.
     *
     * @param versionId   The version of the artifacts to retrieve.
     * @param artifactIds The ids of the artifact to retrieve.
     * @return List of {@link ArtifactAppEntity} for each given id.
     * @throws SafaError If authenticated user does not have permission to view this project.
     */
    @GetMapping(AppRoutes.Retrieval.GET_ARTIFACT_IDS_IN_VERSION)
    public List<ArtifactAppEntity> queryArtifactInVersion(@PathVariable UUID versionId,
                                                          @RequestBody List<UUID> artifactIds) throws SafaError {
        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
        ProjectVersion projectVersion = getResourceBuilder().fetchVersion(versionId)
                .withPermission(ProjectPermission.VIEW, user).get();
        return getServiceProvider().getArtifactService().getAppEntitiesByIds(projectVersion, user, artifactIds);
    }

    /**
     * Returns the current list of traces in the specified project version.
     *
     * @param versionId The UUID of the version whose traces are returned
     * @return List of trace app entities existing in specified version.
     * @throws SafaError Throws error is authorized user does not have read permission on the project.
     */
    @GetMapping(AppRoutes.Retrieval.GET_TRACES_IN_VERSION)
    public List<TraceAppEntity> getTracesInVersion(@PathVariable UUID versionId) throws SafaError {
        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
        ProjectVersion projectVersion = getResourceBuilder().fetchVersion(versionId)
                .withPermission(ProjectPermission.VIEW, user).get();
        return getServiceProvider().getTraceService().getAppEntities(projectVersion, user);
    }
}
