package edu.nd.crc.safa.server.services;

import java.util.List;

import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.CommitError;
import edu.nd.crc.safa.server.entities.db.ProjectParsingActivities;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.server.repositories.CommitErrorRepository;
import edu.nd.crc.safa.server.repositories.TraceLinkVersionRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Responsible for providing an interface to modify artifacts in a project by calculating
 * and storing their changes between the previous version.
 *
 * @author Alberto Rodriguez
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
     * @return List of commit errors occurring while attempting to commit artifacts.
     * @throws SafaError Throws error if any database related errors arise during saving the new artifacts/
     */
    public List<CommitError> commitVersionArtifacts(ProjectVersion projectVersion,
                                                    List<ArtifactAppEntity> projectArtifacts) throws SafaError {
        List<CommitError> commitErrors = this.artifactVersionRepository
            .commitAllEntitiesInProjectVersion(projectVersion, projectArtifacts);
        for (CommitError commitError : commitErrors) {
            commitError.setApplicationActivity(ProjectParsingActivities.PARSING_ARTIFACTS);
            this.commitErrorRepository.save(commitError);
        }
        return commitErrors;
    }

    /**
     * Calculates the changes in each trace from the previous versions and stores
     * changes at given ProjectVersion.
     *
     * @param projectVersion The ProjectVersion associated with calculated artifact changes.
     * @param traces         List of artifact's in a project whose version will be stored.
     * @return List of errors occurring while committing traces.
     * @throws SafaError Throws error if any database related errors arise during saving the new artifacts/
     */
    public List<CommitError> commitVersionTraces(ProjectVersion projectVersion,
                                                 List<TraceAppEntity> traces) throws SafaError {
        List<CommitError> commitErrors = this.traceLinkVersionRepository
            .commitAllEntitiesInProjectVersion(projectVersion, traces);

        for (CommitError commitError : commitErrors) {
            commitError.setApplicationActivity(ProjectParsingActivities.PARSING_TRACES);
            this.commitErrorRepository.save(commitError);
        }
        return commitErrors;
    }
}
