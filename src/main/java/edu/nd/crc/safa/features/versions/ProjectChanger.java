package edu.nd.crc.safa.features.versions;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.IVersionEntity;
import edu.nd.crc.safa.features.common.ProjectEntities;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.errors.entities.db.CommitError;
import edu.nd.crc.safa.features.layout.entities.app.LayoutManager;
import edu.nd.crc.safa.features.notifications.builders.AbstractEntityChangeBuilder;
import edu.nd.crc.safa.features.notifications.builders.EntityChangeBuilder;
import edu.nd.crc.safa.features.notifications.builders.ProjectVersionChangeBuilder;
import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.ProjectEntityType;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import org.javatuples.Pair;

/**
 * Responsible for managing change and performing layout updates.
 */
@AllArgsConstructor
public class ProjectChanger {

    /**
     * The version being changed.
     */
    private ProjectVersion projectVersion;
    /**
     * Provides artifact and trace version repositories
     */
    private ServiceProvider serviceProvider;

    /**
     * Performs modifications specified in project commit and updates the layout accordingly.
     *
     * @param projectCommitDefinition Commit containing addition, modifications, and deletions of entities.
     * @param user                    The user performing the commit
     * @return {@link ProjectCommitDefinition} Commit containing persisted entities and any errors.
     */
    public ProjectCommitAppEntity commit(SafaUser user, ProjectCommitDefinition projectCommitDefinition) {
        ProjectCommitAppEntity committedChanges = serviceProvider
            .getCommitService()
            .performCommit(projectCommitDefinition, user);

        if (projectCommitDefinition.shouldUpdateDefaultLayout()) {
            LayoutManager layoutManager = new LayoutManager(serviceProvider, projectVersion, user);
            layoutManager.generateLayoutUpdates(committedChanges);
        }

        return committedChanges;
    }

    /**
     * Sets given entities as the only entities existing in project version.
     * Detects deleted entities by noting which entities are missing that were previously defined.
     *
     * @param projectEntities Artifact and trace links to set.
     * @param user            User making the request
     */
    public void setEntitiesAsCompleteSet(ProjectEntities projectEntities, SafaUser user) {
        List<ArtifactAppEntity> artifacts = projectEntities.getArtifacts();
        List<TraceAppEntity> traces = projectEntities.getTraces();
        List<Pair<ArtifactVersion, CommitError>> artifactResponse = serviceProvider
            .getArtifactVersionRepository()
            .commitAllAppEntitiesToProjectVersion(projectVersion, artifacts, true, user);
        List<Pair<TraceLinkVersion, CommitError>> traceResponse = serviceProvider.getTraceLinkVersionRepository()
            .commitAllAppEntitiesToProjectVersion(projectVersion, traces, true, user);
        saveCommitErrors(artifactResponse, ProjectEntityType.ARTIFACTS);
        saveCommitErrors(traceResponse, ProjectEntityType.TRACES);

        LayoutManager layoutManager = new LayoutManager(serviceProvider, projectVersion, user);
        layoutManager.generateLayoutForProject();

        AbstractEntityChangeBuilder changeBuilder = createChangeNotification(user, artifactResponse,
            artifacts, traceResponse, traces);
        this.serviceProvider.getNotificationService().broadcastChange(changeBuilder);
    }

    private <T> void saveCommitErrors(List<Pair<T, CommitError>> commitResponse,
                                      ProjectEntityType projectEntityType) {
        for (Pair<T, CommitError> payload : commitResponse) {
            CommitError commitError = payload.getValue1();
            if (commitError != null) {
                commitError.setApplicationActivity(projectEntityType);
                this.serviceProvider
                    .getCommitErrorRepository()
                    .save(commitError);
            }
        }
    }

    public ProjectVersionChangeBuilder createChangeNotification(
        SafaUser user,
        List<Pair<ArtifactVersion, CommitError>> artifactResponse,
        List<ArtifactAppEntity> artifacts,
        List<Pair<TraceLinkVersion, CommitError>> traceResponse,
        List<TraceAppEntity> traces
    ) {
        List<UUID> removedArtifactIds = getEntitiesInResponse(artifactResponse, ModificationType.REMOVED);
        List<UUID> modifiedArtifactIds = getEntitiesInResponse(artifactResponse, ModificationType.ADDED);
        modifiedArtifactIds.addAll(getEntitiesInResponse(artifactResponse, ModificationType.MODIFIED));

        List<UUID> removedTraceIds = getEntitiesInResponse(traceResponse, ModificationType.REMOVED);
        List<UUID> modifiedTraceIds = getEntitiesInResponse(traceResponse, ModificationType.ADDED);
        boolean shouldUpdateLayout = !modifiedTraceIds.isEmpty();
        modifiedTraceIds.addAll(getEntitiesInResponse(traceResponse, ModificationType.MODIFIED));


        return EntityChangeBuilder
            .create(user, projectVersion)
            .withArtifactsDelete(removedArtifactIds)
            .withArtifactsUpdate(artifacts)
            .withTracesDelete(removedTraceIds)
            .withTracesUpdate(traces)
            .withUpdateLayout(shouldUpdateLayout);
    }

    public <A extends IAppEntity, T extends IVersionEntity<A>> List<UUID> getEntitiesInResponse(
        List<Pair<T, CommitError>> response,
        ModificationType modificationType) {
        return response
            .stream()
            .map(Pair::getValue0)
            .filter(a -> a.getModificationType().equals(modificationType))
            .map(IVersionEntity::getBaseEntityId)
            .collect(Collectors.toList());
    }
}
