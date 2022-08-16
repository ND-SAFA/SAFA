package edu.nd.crc.safa.features.commits.services;

import java.util.List;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.features.errors.entities.db.CommitError;
import edu.nd.crc.safa.features.errors.repositories.CommitErrorRepository;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.ProjectEntity;
import edu.nd.crc.safa.features.projects.services.AppEntityRetrievalService;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.features.traces.repositories.TraceLinkVersionRepository;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import org.javatuples.Pair;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;


/**
 * Provides a layer of abstraction above a commit for setting artifacts and traces at a version.w
 */
@Service
@Scope("singleton")
public class EntityVersionService {

    private final ArtifactVersionRepository artifactVersionRepository;
    private final TraceLinkVersionRepository traceLinkVersionRepository;
    private final CommitErrorRepository commitErrorRepository;
    private final AppEntityRetrievalService appEntityRetrievalService;

    @Autowired
    public EntityVersionService(ArtifactVersionRepository artifactVersionRepository,
                                TraceLinkVersionRepository traceLinkVersionRepository,
                                CommitErrorRepository commitErrorRepository,
                                AppEntityRetrievalService appEntityRetrievalService) {
        this.artifactVersionRepository = artifactVersionRepository;
        this.commitErrorRepository = commitErrorRepository;
        this.traceLinkVersionRepository = traceLinkVersionRepository;
        this.appEntityRetrievalService = appEntityRetrievalService;
    }

    /**
     * Saves given artifacts and traces to given version. Note, if given version
     * already contains records of given entities, they are replaced.
     *
     * @param projectVersion The version to store the entities to.
     * @param artifacts      The artifacts to store to version.
     * @param traces         The traces to store to version.
     * @param asCompleteSet  Whether traces should be set
     * @throws SafaError Throws error is a problem occurs while saving artifacts or traces.
     */
    @Transactional
    public void setProjectEntitiesAtVersion(ProjectVersion projectVersion,
                                            @NotNull List<ArtifactAppEntity> artifacts,
                                            @NotNull List<TraceAppEntity> traces,
                                            boolean asCompleteSet) throws SafaError {
        this.addArtifactsAtVersionAndSaveErrors(projectVersion, artifacts, asCompleteSet);
        this.setTracesAtVersionAndSaveErrors(projectVersion, traces, asCompleteSet);
        appEntityRetrievalService.retrieveProjectAppEntityAtProjectVersion(projectVersion);
    }

    /**
     * Calculates the changes in each artifact body from the previous versions and stores
     * changes at given ProjectVersion.
     *
     * @param projectVersion   The ProjectVersion associated with calculated artifact changes.
     * @param projectArtifacts List of artifact's in a project whose version will be stored.
     * @param setAsCompleteSet Whether given entities should be created as complete set of artifacts at version.
     * @throws SafaError Throws error if any database related errors arise during saving the new artifacts/
     */
    public void addArtifactsAtVersionAndSaveErrors(ProjectVersion projectVersion,
                                                   List<ArtifactAppEntity> projectArtifacts,
                                                   boolean setAsCompleteSet) throws SafaError {
        List<Pair<ArtifactVersion, CommitError>> commitResponse = this.artifactVersionRepository
            .commitAllAppEntitiesToProjectVersion(projectVersion, projectArtifacts, setAsCompleteSet);
        for (Pair<ArtifactVersion, CommitError> commitPayload : commitResponse) {
            CommitError commitError = commitPayload.getValue1();
            if (commitError != null) {
                commitError.setApplicationActivity(ProjectEntity.ARTIFACTS);
                this.commitErrorRepository.save(commitError);
            }
        }
    }

    /**
     * Calculates the changes in each trace from the previous versions and stores
     * changes at given ProjectVersion.
     *
     * @param projectVersion   The ProjectVersion associated with calculated artifact changes.
     * @param traces           List of artifact's in a project whose version will be stored.
     * @param setAsCompleteSet Whether given traces should be treated as entire set of traces in version.
     * @throws SafaError Throws error if any database related errors arise during saving the new artifacts/
     */
    public void setTracesAtVersionAndSaveErrors(ProjectVersion projectVersion,
                                                List<TraceAppEntity> traces,
                                                boolean setAsCompleteSet) throws SafaError {
        List<Pair<TraceLinkVersion, CommitError>> commitResponse = this.traceLinkVersionRepository
            .commitAllAppEntitiesToProjectVersion(projectVersion, traces, setAsCompleteSet);

        for (Pair<TraceLinkVersion, CommitError> payload : commitResponse) {
            CommitError commitError = payload.getValue1();
            if (commitError != null) {
                commitError.setApplicationActivity(ProjectEntity.TRACES);
                this.commitErrorRepository.save(commitError);
            }
        }
    }
}
