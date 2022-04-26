package edu.nd.crc.safa.server.services;

import java.util.List;

import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.CommitError;
import edu.nd.crc.safa.server.entities.db.ProjectParsingActivities;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.server.repositories.CommitErrorRepository;
import edu.nd.crc.safa.server.repositories.artifacts.ArtifactVersionRepository;
import edu.nd.crc.safa.server.repositories.traces.TraceLinkVersionRepository;

import org.javatuples.Pair;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;


/**
 * Provides a layer of abstraction above a commit for setting artifacts and traces at a version.w
 */
@Service
public class EntityVersionService {

    private final ArtifactVersionRepository artifactVersionRepository;
    private final TraceLinkVersionRepository traceLinkVersionRepository;
    private final CommitErrorRepository commitErrorRepository;

    @Autowired
    public EntityVersionService(ArtifactVersionRepository artifactVersionRepository,
                                TraceLinkVersionRepository traceLinkVersionRepository,
                                CommitErrorRepository commitErrorRepository) {
        this.artifactVersionRepository = artifactVersionRepository;
        this.commitErrorRepository = commitErrorRepository;
        this.traceLinkVersionRepository = traceLinkVersionRepository;
    }

    /**
     * Calculates the changes in each artifact body from the previous versions and stores
     * changes at given ProjectVersion.
     *
     * @param projectVersion   The ProjectVersion associated with calculated artifact changes.
     * @param projectArtifacts List of artifact's in a project whose version will be stored.
     * @throws SafaError Throws error if any database related errors arise during saving the new artifacts/
     */
    public void commitVersionArtifacts(ProjectVersion projectVersion,
                                       List<ArtifactAppEntity> projectArtifacts) throws SafaError {
        List<Pair<ArtifactVersion, CommitError>> commitResponse = this.artifactVersionRepository
            .commitAllAppEntitiesToProjectVersion(projectVersion, projectArtifacts);
        for (Pair<ArtifactVersion, CommitError> commitPayload : commitResponse) {
            CommitError commitError = commitPayload.getValue1();
            if (commitError != null) {
                commitError.setApplicationActivity(ProjectParsingActivities.PARSING_ARTIFACTS);
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
    public void commitVersionTraces(ProjectVersion projectVersion,
                                    List<TraceAppEntity> traces) throws SafaError {
        List<Pair<TraceLinkVersion, CommitError>> commitResponse = this.traceLinkVersionRepository
            .commitAllAppEntitiesToProjectVersion(projectVersion, traces);

        for (Pair<TraceLinkVersion, CommitError> payload : commitResponse) {
            CommitError commitError = payload.getValue1();
            if (commitError != null) {
                commitError.setApplicationActivity(ProjectParsingActivities.PARSING_TRACES);
                this.commitErrorRepository.save(commitError);
            }
        }
    }
}
