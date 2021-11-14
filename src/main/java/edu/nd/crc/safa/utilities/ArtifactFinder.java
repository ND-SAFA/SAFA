package edu.nd.crc.safa.utilities;

import java.util.Optional;

import edu.nd.crc.safa.server.entities.db.Artifact;

public interface ArtifactFinder {
    Optional<Artifact> findArtifact(String artifactName);
}
