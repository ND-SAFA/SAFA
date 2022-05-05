package edu.nd.crc.safa.server.services;

import java.util.List;
import javax.annotation.PostConstruct;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.server.entities.api.ProjectEntities;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.CommitError;
import edu.nd.crc.safa.server.entities.db.Job;
import edu.nd.crc.safa.server.entities.db.ProjectEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.server.repositories.CommitErrorRepository;
import edu.nd.crc.safa.server.repositories.artifacts.ArtifactVersionRepository;
import edu.nd.crc.safa.server.repositories.traces.TraceLinkVersionRepository;
import edu.nd.crc.safa.server.services.retrieval.AppEntityRetrievalService;

import org.javatuples.Pair;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;


/**
 * Responsible for providing an interface to modify artifacts in a project by calculating
 * and storing their changes between the previous version.
 *
 * @author Alberto Rodriguez
 */
@Service
public class EntityVersionService {

    public static EntityVersionService instance;
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

    public static EntityVersionService getInstance() {
        return instance;
    }

    /**
     * Saves given artifacts and traces to given version. Note, if given version
     * already contains records of given entities, they are replaced.
     *
     * @param projectVersion The version to store the entities to.
     * @param artifacts      The artifacts to store to version.
     * @param traces         The traces to store to version.
     * @return ProjectEntities representing current state of project version after modification.
     * @throws SafaError Throws error is a problem occurs while saving artifacts or traces.
     */
    @Transactional
    public ProjectEntities setProjectEntitiesAtVersion(ProjectVersion projectVersion,
                                                       @NotNull List<ArtifactAppEntity> artifacts,
                                                       @NotNull List<TraceAppEntity> traces) throws SafaError {
        this.setArtifactsAtVersionAndSaveErrors(projectVersion, artifacts);
        this.setTracesAtVersionAndSaveErrors(projectVersion, traces);
        return appEntityRetrievalService.retrieveProjectEntitiesAtProjectVersion(projectVersion);
    }

    @Transactional
    public ProjectEntities setProjectEntitiesAtVersion(ProjectVersion projectVersion,
                                                       @NotNull List<ArtifactAppEntity> artifacts,
                                                       @NotNull List<TraceAppEntity> traces,
                                                       Job job) throws SafaError {
        int totalEntities = artifacts.size() + traces.size();
        int artifactStepProgress = (int) (artifacts.size() / (double) totalEntities) * 90;
        int traceStepProgress = (int) (artifacts.size() / (double) totalEntities) * 90;

        this.setArtifactsAtVersionAndSaveErrors(projectVersion, artifacts);
        this.setTracesAtVersionAndSaveErrors(projectVersion, traces);

        return appEntityRetrievalService.retrieveProjectEntitiesAtProjectVersion(projectVersion);
    }

    /**
     * Calculates the changes in each artifact body from the previous versions and stores
     * changes at given ProjectVersion.
     *
     * @param projectVersion   The ProjectVersion associated with calculated artifact changes.
     * @param projectArtifacts List of artifact's in a project whose version will be stored.
     * @throws SafaError Throws error if any database related errors arise during saving the new artifacts/
     */
    public void setArtifactsAtVersionAndSaveErrors(ProjectVersion projectVersion,
                                                   List<ArtifactAppEntity> projectArtifacts) throws SafaError {
        List<Pair<ArtifactVersion, CommitError>> commitResponse = this.artifactVersionRepository
            .commitAllAppEntitiesToProjectVersion(projectVersion, projectArtifacts);
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
     * @param projectVersion The ProjectVersion associated with calculated artifact changes.
     * @param traces         List of artifact's in a project whose version will be stored.
     * @throws SafaError Throws error if any database related errors arise during saving the new artifacts/
     */
    public void setTracesAtVersionAndSaveErrors(ProjectVersion projectVersion,
                                                List<TraceAppEntity> traces) throws SafaError {
        List<Pair<TraceLinkVersion, CommitError>> commitResponse = this.traceLinkVersionRepository
            .commitAllAppEntitiesToProjectVersion(projectVersion, traces);

        for (Pair<TraceLinkVersion, CommitError> payload : commitResponse) {
            CommitError commitError = payload.getValue1();
            if (commitError != null) {
                commitError.setApplicationActivity(ProjectEntity.TRACES);
                this.commitErrorRepository.save(commitError);
            }
        }
    }

    @PostConstruct
    void init() {
        instance = this;
    }

}
