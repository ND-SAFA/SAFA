package edu.nd.crc.safa.server.controllers;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.AppEntityCreator;
import edu.nd.crc.safa.server.entities.api.CommitAction;
import edu.nd.crc.safa.server.entities.api.ProjectChange;
import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.IAppEntity;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.app.VersionEntityTypes;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.CommitError;
import edu.nd.crc.safa.server.entities.db.IVersionEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.artifacts.ArtifactVersionRepository;
import edu.nd.crc.safa.server.repositories.artifacts.IVersionRepository;
import edu.nd.crc.safa.server.repositories.traces.TraceLinkVersionRepository;
import edu.nd.crc.safa.server.services.NotificationService;
import edu.nd.crc.safa.server.services.retrieval.AppEntityRetrievalService;

import org.javatuples.Pair;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/**
 * Provides endpoints for commit a versioned change to a project's entities.
 */
@RestController
public class CommitController extends BaseController {

    private final ArtifactVersionRepository artifactVersionRepository;
    private final TraceLinkVersionRepository traceLinkVersionRepository;
    private final AppEntityRetrievalService appEntityRetrievalService;
    private final NotificationService notificationService;

    @Autowired
    public CommitController(ResourceBuilder resourceBuilder,
                            ArtifactVersionRepository artifactVersionRepository,
                            TraceLinkVersionRepository traceLinkVersionRepository,
                            AppEntityRetrievalService appEntityRetrievalService,
                            NotificationService notificationService
    ) {
        super(resourceBuilder);
        this.traceLinkVersionRepository = traceLinkVersionRepository;
        this.artifactVersionRepository = artifactVersionRepository;
        this.appEntityRetrievalService = appEntityRetrievalService;
        this.notificationService = notificationService;
    }

    /**
     * Saves given entities to specified project version.
     *
     * @param versionId     The id of the version to commit to.
     * @param projectCommit The entities to commit.
     * @return ProjectCommit The commit containing the entities with any processing additions.
     * @throws SafaError Throws error if user does not have edit permissions on project.
     */
    @PostMapping(AppRoutes.Projects.Commits.commitChange)
    public ProjectCommit commitChange(@PathVariable UUID versionId,
                                      @RequestBody ProjectCommit projectCommit) throws SafaError {
        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withEditVersion();

        // Pre-processing: Add related trace links to be removed.
        for (ArtifactAppEntity artifactAppEntity : projectCommit.getArtifacts().getRemoved()) {
            List<TraceAppEntity> associatedLinks = this.appEntityRetrievalService
                .getTracesInProjectVersionRelatedToArtifact(projectVersion, artifactAppEntity.getName());
            projectCommit.addTraceToDelete(associatedLinks);
        }

        // Commit artifact and trace changes.
        ProjectChange<ArtifactAppEntity> artifactChanges = commitArtifactChanges(projectVersion,
            projectCommit.getArtifacts());

        ProjectChange<TraceAppEntity> traceChanges = commitChanges(projectVersion, projectCommit.getTraces());

        if (artifactChanges.getSize() > 0) {
            this.notificationService.broadUpdateProjectVersionMessage(projectVersion, VersionEntityTypes.ARTIFACTS);
        }
        if (traceChanges.getSize() > 0) {
            this.notificationService.broadUpdateProjectVersionMessage(projectVersion, VersionEntityTypes.TRACES);
        }
        if (artifactChanges.getSize() + traceChanges.getSize() > 0) {
            this.notificationService.broadUpdateProjectVersionMessage(projectVersion, VersionEntityTypes.WARNINGS);
        }
        return new ProjectCommit(projectVersion, artifactChanges, traceChanges);
    }

    private ProjectChange<ArtifactAppEntity> commitArtifactChanges(
        ProjectVersion projectVersion,
        ProjectChange<ArtifactAppEntity> artifacts) throws SafaError {
        return commitChanges(
            projectVersion,
            artifacts,
            this.artifactVersionRepository,
            this.artifactVersionRepository::retrieveAppEntityFromVersionEntity);
    }

    private ProjectChange<TraceAppEntity> commitChanges(ProjectVersion projectVersion,
                                                        ProjectChange<TraceAppEntity> traces) throws SafaError {
        return commitChanges(
            projectVersion,
            traces,
            this.traceLinkVersionRepository,
            this.traceLinkVersionRepository::retrieveAppEntityFromVersionEntity);
    }

    /**
     * Creates any added entities, saves any modified entities, and marks entities removed.
     *
     * @param projectVersion     The project version that should notified of the changes.
     * @param projectChange      The entities that are being touched.
     * @param versionRepository  The IVersionRepository used for this entity.
     * @param appEntityCreator   The constructor for creating app entities from version entities.
     * @param versionEntityTypes The type of version entities that are being updated.
     * @param <AppEntity>        The entity used on the application side.
     * @param <VersionEntity>    The entity used for version control.
     * @return ProjectChange containing processed entities.
     * @throws SafaError Throws error if anything goes wrong during any commit.
     */
    private <AppEntity extends IAppEntity,
        VersionEntity extends IVersionEntity<AppEntity>> ProjectChange<AppEntity> commitChanges(
        ProjectVersion projectVersion,
        ProjectChange<AppEntity> projectChange,
        IVersionRepository<VersionEntity, AppEntity> versionRepository,
        AppEntityCreator<AppEntity, VersionEntity> appEntityCreator,
        VersionEntityTypes versionEntityTypes
    ) throws SafaError {
        ProjectChange<AppEntity> change = new ProjectChange<>();

        // Define actions
        CommitAction<AppEntity, VersionEntity> saveOrModifyAction = (appEntity) ->
            versionRepository.commitSingleEntityToProjectVersion(projectVersion, appEntity);
        CommitAction<AppEntity, VersionEntity> removeAction = (appEntity) ->
            versionRepository.deleteVersionEntityByBaseEntityId(projectVersion, appEntity.getId());

        // Commit added entities
        List<AppEntity> entitiesAdded = commitActionOnAppEntities(
            projectChange.getAdded(),
            saveOrModifyAction,
            appEntityCreator
        );
        change.getAdded().addAll(entitiesAdded);

        // Commit modified entities
        List<AppEntity> entitiesModified = commitActionOnAppEntities(
            projectChange.getModified(),
            saveOrModifyAction,
            appEntityCreator
        );
        change.getModified().addAll(entitiesModified);

        // Commit removed entities
        List<AppEntity> entitiesRemoved = commitActionOnAppEntities(
            projectChange.getRemoved(),
            removeAction,
            appEntityCreator
        );
        change.getRemoved().addAll(entitiesRemoved);
        return change;
    }

    /**
     * Performs given commit action on list of app entities. Uses AppEntityCreator to convert
     * returned version entities into app entities.
     *
     * @param appEntities      The app entities to perform action on.
     * @param commitAction     The commit action applies to each app entity.
     * @param appEntityCreator The AppEntityCreator used to rebuild app entities from resulting version entities.
     * @param <AppEntity>      The Application side entity to process.
     * @param <VersionEntity>  The version entity of the base entity being processed.
     * @return List of processed app entities.
     * @throws SafaError Throws error is anything goes wrong during commit.
     */
    private <AppEntity, VersionEntity> List<AppEntity> commitActionOnAppEntities(
        List<AppEntity> appEntities,
        CommitAction<AppEntity, VersionEntity> commitAction,
        AppEntityCreator<AppEntity, VersionEntity> appEntityCreator
    ) throws SafaError {
        List<AppEntity> updatedEntities = new ArrayList<>();
        for (AppEntity appEntity : appEntities) {
            Pair<VersionEntity, CommitError> commitResponse = commitAction.commitAction(appEntity);

            CommitError commitError = commitResponse.getValue1();
            if (commitError != null) {
                throw new SafaError(commitError.getDescription());
            } else {
                VersionEntity versionEntity = commitResponse.getValue0();
                AppEntity traceAppEntity = appEntityCreator.createAppEntity(versionEntity);
                updatedEntities.add(traceAppEntity);
            }
        }
        return updatedEntities;
    }
}
