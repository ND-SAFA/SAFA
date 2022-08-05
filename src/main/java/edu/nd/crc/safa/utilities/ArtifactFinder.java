package edu.nd.crc.safa.utilities;

import java.util.Optional;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;

/**
 * Defines an interface for a lambda defining a search strategy for artifacts by name.
 */
public interface ArtifactFinder {
    Optional<Artifact> findArtifact(String artifactName);
}
