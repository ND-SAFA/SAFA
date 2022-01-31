package edu.nd.crc.safa.server.controllers;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.ProjectChange;
import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.CommitError;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.repositories.TraceLinkVersionRepository;
import edu.nd.crc.safa.server.services.RevisionNotificationService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

/**
 * Provides endpoints for commit a versioned change to a project's entities.
 */
@RestController
public class CommitController extends BaseController {

    private final ArtifactVersionRepository artifactVersionRepository;
    private final TraceLinkVersionRepository traceLinkVersionRepository;
    private final RevisionNotificationService revisionNotificationService;

    @Autowired
    public CommitController(ProjectRepository projectRepository,
                            ProjectVersionRepository projectVersionRepository,
                            ArtifactVersionRepository artifactVersionRepository,
                            TraceLinkVersionRepository traceLinkVersionRepository,
                            ResourceBuilder resourceBuilder,
                            RevisionNotificationService revisionNotificationService
    ) {
        super(projectRepository, projectVersionRepository, resourceBuilder);
        this.traceLinkVersionRepository = traceLinkVersionRepository;
        this.artifactVersionRepository = artifactVersionRepository;
        this.revisionNotificationService = revisionNotificationService;
    }

    /**
     * Saves given entities to specified project version.
     *
     * @param versionId     The id of the version to commit to.
     * @param projectCommit The entities to commit.
     * @throws SafaError Throws error if user does not have edit permissions on project.
     */
    @PostMapping(AppRoutes.Projects.commitChange)
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void commitChange(@PathVariable UUID versionId,
                             @RequestBody ProjectCommit projectCommit) throws SafaError {
        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withEditVersion();
        commitArtifacts(projectVersion, projectCommit.getArtifacts());
        commitTraces(projectVersion, projectCommit.getTraces());
    }

    private void commitArtifacts(ProjectVersion projectVersion,
                                 ProjectChange<ArtifactAppEntity> artifacts) throws SafaError {
        List<ArtifactAppEntity> changedArtifacts = Stream.concat(
                artifacts.getAdded().stream(),
                artifacts.getModified().stream())
            .collect(Collectors.toList());
        List<CommitError> errors = new ArrayList<>();
        for (ArtifactAppEntity artifact : changedArtifacts) {
            CommitError artifactError = this.artifactVersionRepository
                .commitSingleEntityToProjectVersion(projectVersion, artifact);
            if (artifactError != null) {
                throw new SafaError(artifactError.getDescription());
            }
        }
        for (ArtifactAppEntity artifact : artifacts.getRemoved()) {
            CommitError artifactError = this.artifactVersionRepository.deleteVersionEntityByBaseName(projectVersion,
                artifact.name);
            if (artifactError != null) {
                throw new SafaError(artifactError.getDescription());
            }
        }
        this.revisionNotificationService.broadcastUpdateProject(projectVersion);
    }

    private void commitTraces(ProjectVersion projectVersion,
                              ProjectChange<TraceAppEntity> artifacts) throws SafaError {
        List<TraceAppEntity> changedArtifacts = Stream.concat(
                artifacts.getAdded().stream(),
                artifacts.getModified().stream())
            .collect(Collectors.toList());
        List<CommitError> errors = new ArrayList<>();
        for (TraceAppEntity artifact : changedArtifacts) {
            CommitError traceError = this.traceLinkVersionRepository.commitSingleEntityToProjectVersion(projectVersion,
                artifact);
            if (traceError != null) {
                throw new SafaError(traceError.getDescription());
            }
        }
        for (TraceAppEntity trace : artifacts.getRemoved()) {
            CommitError traceError = this.traceLinkVersionRepository.deleteVersionEntityByBaseName(projectVersion,
                trace.traceLinkId);
            if (traceError != null) {
                throw new SafaError(traceError.getDescription());
            }
        }
        this.revisionNotificationService.broadcastUpdateProject(projectVersion);
    }
}
