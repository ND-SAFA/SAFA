package edu.nd.crc.safa.utilities;

import java.util.Optional;

import edu.nd.crc.safa.server.db.entities.sql.Artifact;
import edu.nd.crc.safa.server.db.entities.sql.TraceLink;

public interface TraceLinkFinder {
    Optional<TraceLink> findTrace(Artifact source, Artifact target);
}
