package edu.nd.crc.safa.features.commits.services;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.features.artifacts.repositories.IVersionRepository;
import edu.nd.crc.safa.features.commits.entities.app.CommitAction;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.commits.pipeline.CommitPipeline;
import edu.nd.crc.safa.features.common.EntityParsingResult;
import edu.nd.crc.safa.features.common.IVersionEntity;
import edu.nd.crc.safa.features.delta.entities.app.ProjectChange;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.errors.entities.db.CommitError;
import edu.nd.crc.safa.features.notifications.services.NotificationService;
import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.IAppEntityCreator;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.repositories.ProjectRepository;
import edu.nd.crc.safa.features.traces.repositories.TraceLinkVersionRepository;
import edu.nd.crc.safa.features.traces.services.TraceService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import lombok.Getter;
import org.javatuples.Pair;
import org.springframework.stereotype.Service;

/**
 * Responsible for performing commits.
 */
@Getter
@AllArgsConstructor
@Service
public class CommitService {
    private final TraceService traceService;
    private final ArtifactVersionRepository artifactVersionRepository;
    private final TraceLinkVersionRepository traceLinkVersionRepository;
    private final NotificationService notificationService;
    private final ProjectRepository projectRepository;
    private final SafaUserService safaUserService;

    /**
     * Saves entities in commit to specified project version.
     *
     * @param projectCommitDefinition The commit containing changes to artifacts and traces.
     * @param user                    The user performing the commit
     * @return ProjectCommit with updated entities.
     * @throws SafaError Throws error if any change fails to commit.
     */
    public ProjectCommitAppEntity performCommit(ProjectCommitDefinition projectCommitDefinition,
                                                SafaUser user) throws SafaError {
        projectCommitDefinition.setUser(user);
        CommitPipeline pipeline = new CommitPipeline(projectCommitDefinition);
        return pipeline.commit(this);
    }

    /**
     * Saves the artifacts under the project version with given modification type.
     *
     * @param user             The user saving the artifacts.
     * @param projectVersion   The project version to save to.
     * @param artifacts        The artifacts to save.
     * @param modificationType The modification type to store them under.
     * @return The project commit.
     */
    public ProjectCommitAppEntity saveArtifacts(SafaUser user,
                                                ProjectVersion projectVersion,
                                                List<ArtifactAppEntity> artifacts,
                                                ModificationType modificationType) {
        ProjectCommitDefinition projectCommitDefinition = new ProjectCommitDefinition();
        projectCommitDefinition.setCommitVersion(projectVersion);
        projectCommitDefinition.addArtifacts(modificationType, artifacts);
        return this.performCommit(projectCommitDefinition, user);
    }

    /**
     * Creates any added entities, saves any modified entities, and marks entities removed.
     *
     * @param projectVersion          The project version that should be notified of the changes.
     * @param projectChange           The entities that are being touched.
     * @param versionEntityRepository The IVersionRepository used for this entity.
     * @param iAppEntityCreator       The constructor for creating app entities from version entities.
     * @param user                    The user making the change
     * @param failOnError             Whether error should be thrown if encountered.
     * @param <A>                     The entity used on the application side.
     * @param <V>                     The entity used for version control.
     * @return ProjectChange containing processed entities.
     * @throws SafaError Throws error if anything goes wrong during any commit.
     */
    public <A extends IAppEntity,
        V extends IVersionEntity<A>> Pair<ProjectChange<A>,
        List<CommitError>> commitEntityChanges(
        ProjectVersion projectVersion,
        ProjectChange<A> projectChange,
        IVersionRepository<V, A> versionEntityRepository,
        IAppEntityCreator<A, V> iAppEntityCreator,
        boolean failOnError,
        SafaUser user
    ) throws SafaError {
        ProjectChange<A> processedChange = new ProjectChange<>();
        List<CommitError> commitErrors;

        List<UUID> baseEntityIds = projectChange.getEntityIds();
        Map<UUID, List<V>> entityHashTable = versionEntityRepository.createVersionEntityMap(projectVersion,
            baseEntityIds);
        // Define actions
        CommitAction<A, V> saveOrModifyAction = a ->
            versionEntityRepository.commitAppEntityToProjectVersion(projectVersion, a, user, entityHashTable);
        CommitAction<A, V> deleteAction = a ->
            versionEntityRepository.deleteVersionEntityByBaseEntityId(projectVersion, a.getId(), user, entityHashTable);

        // Commit added entities
        EntityParsingResult<A, CommitError> addedResponse = commitActionOnAppEntities(
            projectChange.getAdded(),
            saveOrModifyAction,
            iAppEntityCreator,
            failOnError
        );
        List<A> entitiesAdded = addedResponse.getEntities();
        processedChange.getAdded().addAll(entitiesAdded);
        commitErrors = new ArrayList<>(addedResponse.getErrors());

        // Commit modified entities
        EntityParsingResult<A, CommitError> modifiedResponse = commitActionOnAppEntities(
            projectChange.getModified(),
            saveOrModifyAction,
            iAppEntityCreator,
            failOnError
        );
        List<A> entitiesModified = modifiedResponse.getEntities();
        processedChange.getModified().addAll(entitiesModified);
        commitErrors.addAll(modifiedResponse.getErrors());

        // Commit deleted entities
        System.out.println("Entities to delete:" + projectChange.getRemoved());
        EntityParsingResult<A, CommitError> removeResponse = commitActionOnAppEntities(
            projectChange.getRemoved(),
            deleteAction,
            iAppEntityCreator,
            failOnError
        );
        List<A> entitiesRemoved = removeResponse.getEntities();
        processedChange.getRemoved().addAll(entitiesRemoved);
        commitErrors.addAll(removeResponse.getErrors());
        return new Pair<>(processedChange, commitErrors);
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
