package edu.nd.crc.safa.server.services;

import java.util.List;

import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.ParserError;
import edu.nd.crc.safa.server.entities.db.ProjectParsingActivities;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.server.repositories.ParserErrorRepository;
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

    ArtifactVersionRepository artifactVersionRepository;
    TraceLinkVersionRepository traceLinkVersionRepository;
    ParserErrorRepository parserErrorRepository;

    DeltaService deltaService;

    String bar = "-------------------------------------";

    @Autowired
    public EntityVersionService(ArtifactVersionRepository artifactVersionRepository,
                                TraceLinkVersionRepository traceLinkVersionRepository,
                                ParserErrorRepository parserErrorRepository,
                                DeltaService deltaService) {
        this.artifactVersionRepository = artifactVersionRepository;
        this.parserErrorRepository = parserErrorRepository;
        this.traceLinkVersionRepository = traceLinkVersionRepository;
        this.deltaService = deltaService;
    }

    /**
     * Calculates the changes in each artifact body from the previous versions and stores
     * changes at given ProjectVersion.
     *
     * @param projectVersion   The ProjectVersion associated with calculated artifact changes.
     * @param projectArtifacts List of artifact's in a project whose version will be stored.
     * @throws SafaError Throws error if any database related errors arise during saving the new artifacts/
     */
    public void setArtifactsAtVersion(ProjectVersion projectVersion,
                                      List<ArtifactAppEntity> projectArtifacts) throws SafaError {
        List<ParserError> parserErrors = this.artifactVersionRepository
            .commitAppEntitiesToProjectVersion(projectVersion, projectArtifacts);
        for (ParserError parserError : parserErrors) {
            parserError.setApplicationActivity(ProjectParsingActivities.PARSING_ARTIFACTS);
            this.parserErrorRepository.save(parserError);
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
    public void setTracesAtVersion(ProjectVersion projectVersion,
                                   List<TraceAppEntity> traces) throws SafaError {
        System.out.println("START TRACE VERSIONING:" + traces.size() + bar);
        List<ParserError> parserErrors = this.traceLinkVersionRepository
            .commitAppEntitiesToProjectVersion(projectVersion, traces);
        System.out.println("PARSER ERRORS:" + parserErrors + bar);

        for (ParserError parserError : parserErrors) {
            parserError.setApplicationActivity(ProjectParsingActivities.PARSING_TRACES);
            this.parserErrorRepository.save(parserError);
        }
    }
}
