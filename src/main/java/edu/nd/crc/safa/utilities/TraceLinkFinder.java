package edu.nd.crc.safa.utilities;

import java.util.Optional;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.traces.entities.db.TraceLinkVersion;

/**
 * Defines an interface for defining lambdas for querying for traces.
 */
public interface TraceLinkFinder {
    Optional<TraceLinkVersion> findTrace(Artifact source, Artifact target);
}
