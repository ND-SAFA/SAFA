package edu.nd.crc.safa.features.versions;

import java.util.List;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ProjectEntities;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.errors.entities.db.CommitError;
import edu.nd.crc.safa.features.layout.entities.app.LayoutManager;
import edu.nd.crc.safa.features.projects.entities.db.ProjectEntity;
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
     * @return {@link ProjectCommitDefinition} Commit containing persisted entities and any errors.
     */
    public ProjectCommitAppEntity commit(ProjectCommitDefinition projectCommitDefinition) {
        return commitAsUser(projectCommitDefinition, serviceProvider.getSafaUserService().getCurrentUser());
    }

    /**
     * Performs modifications specified in project commit and updates the layout accordingly.
     *
     * @param projectCommitDefinition Commit containing addition, modifications, and deletions of entities.
     * @param user                    The user performing the commit
     * @return {@link ProjectCommitDefinition} Commit containing persisted entities and any errors.
     */
    public ProjectCommitAppEntity commitAsUser(ProjectCommitDefinition projectCommitDefinition, SafaUser user) {
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
        saveCommitErrors(artifactResponse, ProjectEntity.ARTIFACTS);
        saveCommitErrors(traceResponse, ProjectEntity.TRACES);

        LayoutManager layoutManager = new LayoutManager(serviceProvider, projectVersion, user);
        layoutManager.generateLayoutForProject();
    }

    private <T> void saveCommitErrors(List<Pair<T, CommitError>> commitResponse,
                                      ProjectEntity projectEntity) {
        for (Pair<T, CommitError> payload : commitResponse) {
            CommitError commitError = payload.getValue1();
            if (commitError != null) {
                commitError.setApplicationActivity(projectEntity);
                this.serviceProvider
                    .getCommitErrorRepository()
                    .save(commitError);
            }
        }
    }
}
