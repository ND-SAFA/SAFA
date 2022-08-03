package edu.nd.crc.safa.features.commits.services;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.common.EntityParsingResult;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.features.artifacts.repositories.IVersionRepository;
import edu.nd.crc.safa.features.commits.entities.app.CommitAction;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.IVersionEntity;
import edu.nd.crc.safa.features.delta.entities.app.ProjectChange;
import edu.nd.crc.safa.features.errors.entities.db.CommitError;
import edu.nd.crc.safa.features.notifications.NotificationService;
import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.IAppEntityCreator;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.services.AppEntityRetrievalService;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.repositories.TraceLinkVersionRepository;
import edu.nd.crc.safa.features.versions.entities.app.VersionEntityTypes;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import org.javatuples.Pair;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Responsible for performing commits.
 */
@Service
public class CommitService {
    private final ArtifactVersionRepository artifactVersionRepository;
    private final TraceLinkVersionRepository traceLinkVersionRepository;

    private final AppEntityRetrievalService appEntityRetrievalService;
    private final NotificationService notificationService;

    @Autowired
    public CommitService(ArtifactVersionRepository artifactVersionRepository,
                         TraceLinkVersionRepository traceLinkVersionRepository,
                         AppEntityRetrievalService appEntityRetrievalService,
                         NotificationService notificationService) {
        this.appEntityRetrievalService = appEntityRetrievalService;
        this.artifactVersionRepository = artifactVersionRepository;
        this.traceLinkVersionRepository = traceLinkVersionRepository;
        this.notificationService = notificationService;
    }

    /**
     * Saves entities in commit to specified project version.
     *
     * @param projectCommit The commit containing changes to artifacts and traces.
     * @return ProjectCommit with updated entities.
     * @throws SafaError Throws error if any change fails to commit.
     */
    public ProjectCommit performCommit(ProjectCommit projectCommit) throws SafaError {

        ProjectVersion projectVersion = projectCommit.getCommitVersion();
        boolean failOnError = projectCommit.isFailOnError();
        List<CommitError> errors;

        // Pre-processing: Add related trace links to be removed.
        for (ArtifactAppEntity artifact : projectCommit.getArtifacts().getRemoved()) {
            List<TraceAppEntity> linksToArtifact = this.appEntityRetrievalService
                .getTracesInProjectVersionRelatedToArtifact(projectVersion, artifact.getName());
            projectCommit.addRemovedTraces(linksToArtifact);
        }

        // Commit artifact and trace changes.
        Pair<ProjectChange<ArtifactAppEntity>, List<CommitError>> artifactResponse = commitArtifactChanges(
            projectVersion,
            projectCommit.getArtifacts(),
            failOnError);
        errors = new ArrayList<>(artifactResponse.getValue1()); // linter wants it like this for some reason
        ProjectChange<ArtifactAppEntity> artifactChanges = artifactResponse.getValue0();

        Pair<ProjectChange<TraceAppEntity>, List<CommitError>> traceResponse = commitTraceChanges(
            projectVersion,
            projectCommit.getTraces(),
            failOnError);
        ProjectChange<TraceAppEntity> traceChanges = traceResponse.getValue0();
        errors.addAll(traceResponse.getValue1());

        if (artifactChanges.getSize() > 0) {
            this.notificationService.broadUpdateProjectVersionMessage(projectVersion, VersionEntityTypes.ARTIFACTS);
        }
        if (traceChanges.getSize() > 0) {
            this.notificationService.broadUpdateProjectVersionMessage(projectVersion, VersionEntityTypes.TRACES);
        }
        if (artifactChanges.getSize() + traceChanges.getSize() > 0) {
            this.notificationService.broadUpdateProjectVersionMessage(projectVersion, VersionEntityTypes.WARNINGS);
        }
        return new ProjectCommit(projectVersion, artifactChanges, traceChanges, errors, failOnError);
    }

    private Pair<ProjectChange<ArtifactAppEntity>, List<CommitError>> commitArtifactChanges(
        ProjectVersion projectVersion,
        ProjectChange<ArtifactAppEntity> artifacts,
        boolean failOnError) throws SafaError {
        return commitEntityChanges(
            projectVersion,
            artifacts,
            this.artifactVersionRepository,
            this.artifactVersionRepository::retrieveAppEntityFromVersionEntity,
            failOnError);
    }

    private Pair<ProjectChange<TraceAppEntity>, List<CommitError>> commitTraceChanges(
        ProjectVersion projectVersion,
        ProjectChange<TraceAppEntity> traces,
        boolean failOnError) throws SafaError {
        return commitEntityChanges(
            projectVersion,
            traces,
            this.traceLinkVersionRepository,
            this.traceLinkVersionRepository::retrieveAppEntityFromVersionEntity,
            failOnError);
    }

    /**
     * Creates any added entities, saves any modified entities, and marks entities removed.
     *
     * @param projectVersion          The project version that should be notified of the changes.
     * @param projectChange           The entities that are being touched.
     * @param versionEntityRepository The IVersionRepository used for this entity.
     * @param iAppEntityCreator       The constructor for creating app entities from version entities.
     * @param <A>                     The entity used on the application side.
     * @param <V>                     The entity used for version control.
     * @return ProjectChange containing processed entities.
     * @throws SafaError Throws error if anything goes wrong during any commit.
     */
    private <A extends IAppEntity,
        V extends IVersionEntity<A>> Pair<ProjectChange<A>,
        List<CommitError>> commitEntityChanges(
        ProjectVersion projectVersion,
        ProjectChange<A> projectChange,
        IVersionRepository<V, A> versionEntityRepository,
        IAppEntityCreator<A, V> iAppEntityCreator,
        boolean failOnError
    ) throws SafaError {
        ProjectChange<A> change = new ProjectChange<>();
        List<CommitError> commitErrors;

        // Define actions
        CommitAction<A, V> saveOrModifyAction = a ->
            versionEntityRepository.commitAppEntityToProjectVersion(
                projectVersion, a);
        CommitAction<A, V> removeAction = a ->
            versionEntityRepository.deleteVersionEntityByBaseEntityId(
                projectVersion,
                a.getBaseEntityId());

        // Commit added entities
        EntityParsingResult<A, CommitError> addedResponse = commitActionOnAppEntities(
            projectChange.getAdded(),
            saveOrModifyAction,
            iAppEntityCreator,
            failOnError
        );
        List<A> entitiesAdded = addedResponse.getEntities();
        change.getAdded().addAll(entitiesAdded);
        commitErrors = new ArrayList<>(addedResponse.getErrors());

        // Commit modified entities
        EntityParsingResult<A, CommitError> modifiedResponse = commitActionOnAppEntities(
            projectChange.getModified(),
            saveOrModifyAction,
            iAppEntityCreator,
            failOnError
        );
        List<A> entitiesModified = modifiedResponse.getEntities();
        change.getModified().addAll(entitiesModified);

        // Commit removed entities
        EntityParsingResult<A, CommitError> removeResponse = commitActionOnAppEntities(
            projectChange.getRemoved(),
            removeAction,
            iAppEntityCreator,
            failOnError
        );
        List<A> entitiesRemoved = removeResponse.getEntities();
        change.getRemoved().addAll(entitiesRemoved);
        return new Pair<>(change, commitErrors);
    }

    /**
     * Performs given commit action on list of app entities. Uses AppEntityCreator to convert
     * returned version entities into app entities.
     *
     * @param appEntities       The app entities to perform action on.
     * @param commitAction      The commit action applies to each app entity.
     * @param iAppEntityCreator The AppEntityCreator used to rebuild app entities from resulting version entities.
     * @param <A>               The Application side entity to process.
     * @param <V>               The version entity of the base entity being processed.
     * @return List of processed app entities.
     * @throws SafaError Throws error is anything goes wrong during commit.
     */
    private <A, V> EntityParsingResult<A, CommitError> commitActionOnAppEntities(
        List<A> appEntities,
        CommitAction<A, V> commitAction,
        IAppEntityCreator<A, V> iAppEntityCreator,
        boolean failOnError
    ) throws SafaError {
        List<A> updatedEntities = new ArrayList<>();
        List<CommitError> commitErrors = new ArrayList<>();
        for (A a : appEntities) {
            Pair<V, CommitError> commitResponse = commitAction.commitAction(a);

            V v = commitResponse.getValue0();
            CommitError commitError = commitResponse.getValue1();
            if (commitError != null) {
                if (failOnError) {
                    throw new SafaError(commitError.getDescription());
                } else {
                    commitErrors.add(commitError);
                }
            } else if (v != null) {
                A updatedA = iAppEntityCreator.createAppEntity(v);
                updatedEntities.add(updatedA);
            }
        }
        return new EntityParsingResult<>(updatedEntities, commitErrors);
    }
}
