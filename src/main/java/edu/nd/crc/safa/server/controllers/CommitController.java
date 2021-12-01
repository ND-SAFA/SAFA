package edu.nd.crc.safa.server.controllers;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.ProjectChange;
import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.api.ServerError;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.services.ArtifactVersionService;
import edu.nd.crc.safa.server.services.PermissionService;
import edu.nd.crc.safa.server.services.RevisionNotificationService;
import edu.nd.crc.safa.server.services.TraceLinkService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

/**
 * Provides endpoints for commit a versioend change to a project's entities.
 */
@RestController
public class CommitController extends BaseController {

    TraceLinkService traceLinkService;

    ArtifactVersionService artifactVersionService;
    RevisionNotificationService revisionNotificationService;

    @Autowired
    public CommitController(ProjectRepository projectRepository,
                            ProjectVersionRepository projectVersionRepository,
                            PermissionService permissionService,
                            TraceLinkService traceLinkService,
                            ArtifactVersionService artifactVersionService,
                            RevisionNotificationService revisionNotificationService
    ) {
        super(projectRepository, projectVersionRepository, permissionService);
        this.traceLinkService = traceLinkService;
        this.artifactVersionService = artifactVersionService;
        this.revisionNotificationService = revisionNotificationService;
    }

    /**
     * Saves given entities to specified project version.
     *
     * @param versionId     The id of the version to commit to.
     * @param projectCommit The entities to commit.
     * @throws ServerError Throws error if user does not have edit permissions on project.
     */
    @PostMapping(AppRoutes.Projects.commitChange)
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void commitChange(@PathVariable UUID versionId,
                             @RequestBody ProjectCommit projectCommit) throws ServerError {
        ProjectVersion projectVersion = this.projectVersionRepository.findByVersionId(versionId);
        this.permissionService.requireEditPermission(projectVersion.getProject());
        commitArtifacts(projectVersion, projectCommit.getArtifacts());
        commitTraces(projectVersion, projectCommit.getTraces());
    }

    private void commitArtifacts(ProjectVersion projectVersion,
                                 ProjectChange<ArtifactAppEntity> artifacts) throws ServerError {
        List<ArtifactAppEntity> changedArtifacts = Stream.concat(
                artifacts.getAdded().stream(),
                artifacts.getModified().stream())
            .collect(Collectors.toList());
        for (ArtifactAppEntity artifact : changedArtifacts) {
            this.artifactVersionService.setArtifactAtProjectVersion(projectVersion, artifact);
        }
        for (ArtifactAppEntity artifact : artifacts.getRemoved()) {
            this.artifactVersionService.deleteArtifactBody(projectVersion, artifact.name);
        }
        this.revisionNotificationService.broadcastUpdateProject(projectVersion);
    }

    private void commitTraces(ProjectVersion projectVersion, ProjectChange<TraceAppEntity> traces) throws ServerError {
        for (TraceAppEntity trace : traces.getAdded()) {
            traceLinkService.createNewTraceLInk(projectVersion, trace.source, trace.target);
        }
        for (TraceAppEntity trace : traces.getModified()) {
            traceLinkService.updateTraceLink(trace);
        }
        for (TraceAppEntity trace : traces.getRemoved()) {
            traceLinkService.deleteTraceLink(trace);
        }
    }
}
