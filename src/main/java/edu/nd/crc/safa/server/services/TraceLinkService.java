package edu.nd.crc.safa.server.services;

import java.util.Optional;

import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.server.repositories.entities.traces.TraceLinkVersionRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Provides interface to validating and creating trace links.
 */
@Service
public class TraceLinkService {

    private final TraceLinkVersionRepository traceLinkVersionRepository;

    @Autowired
    public TraceLinkService(TraceLinkVersionRepository traceLinkVersionRepository) {
        this.traceLinkVersionRepository = traceLinkVersionRepository;
    }

    public Optional<TraceLinkVersion> queryForLinkBetween(Artifact sourceArtifact, Artifact targetArtifact) {
        Optional<TraceLinkVersion> traceQuery = this.traceLinkVersionRepository
            .getApprovedLinkIfExist(sourceArtifact, targetArtifact);
        if (traceQuery.isPresent()) {
            return traceQuery;
        }
        return this.traceLinkVersionRepository
            .getApprovedLinkIfExist(targetArtifact, sourceArtifact);
    }
}
