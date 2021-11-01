package edu.nd.crc.safa.utilities;

import java.util.Optional;

import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.TraceLink;

public interface TraceLinkFinder {
    Optional<TraceLink> findTrace(Artifact source, Artifact target);
}
