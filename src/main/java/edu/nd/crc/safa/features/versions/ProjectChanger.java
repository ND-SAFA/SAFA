package edu.nd.crc.safa.features.versions;

import java.util.List;

import edu.nd.crc.safa.common.ProjectEntities;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.errors.entities.db.CommitError;
import edu.nd.crc.safa.features.layout.entities.app.LayoutManager;
import edu.nd.crc.safa.features.projects.entities.db.ProjectEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

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
    ProjectVersion projectVersion;
    /**
     * Provides artifact and trace version repositories
     */
    ServiceProvider serviceProvider;

    /**
     * Performs modifications specified in project commit and updates the layout accordingly.
     *
     * @param projectCommit Commit containing addition, modifications, and deletions of entities.
     * @return {@link ProjectCommit} Commit containing persisted entities and any errors.
     */
    public ProjectCommit commit(ProjectCommit projectCommit) {
        ProjectCommit committedChanges = serviceProvider
            .getCommitService()
            .performCommit(projectCommit);
        LayoutManager layoutManager = new LayoutManager(serviceProvider, projectVersion);
        layoutManager.generateLayoutUpdates(committedChanges);
        return committedChanges;
    }

    /**
     * Sets given entities as the only entities existing in project version.
     * Detects deleted entities by noting which entities are missing that were previously defined.
     *
     * @param projectEntities Artifact and trace links to set.
     */
    public void setEntitiesAsCompleteSet(ProjectEntities projectEntities) {
        List<ArtifactAppEntity> artifacts = projectEntities.getArtifacts();
        List<TraceAppEntity> traces = projectEntities.getTraces();
        List<Pair<ArtifactVersion, CommitError>> artifactResponse = serviceProvider
            .getArtifactVersionRepository()
            .commitAllAppEntitiesToProjectVersion(projectVersion, artifacts, true);
        List<Pair<TraceLinkVersion, CommitError>> traceResponse = serviceProvider.getTraceLinkVersionRepository()
            .commitAllAppEntitiesToProjectVersion(projectVersion, traces, true);
        saveCommitErrors(artifactResponse, ProjectEntity.ARTIFACTS);
        saveCommitErrors(traceResponse, ProjectEntity.TRACES);

        Iterable<Artifact> allArtifacts = this.serviceProvider.getArtifactRepository().findAll();
        List<Artifact> projectArtifacts =
            this.serviceProvider.getArtifactRepository().findByProject(projectVersion.getProject());
        Iterable<ArtifactVersion> allVersions = this.serviceProvider.getArtifactVersionRepository().findAll();
        List<ArtifactVersion> projectArtifactVersions =
            this.serviceProvider.getArtifactVersionRepository().findByProjectVersion(projectVersion);

        LayoutManager layoutManager = new LayoutManager(serviceProvider, projectVersion);
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
