package edu.nd.crc.safa.server.entities.db;

import java.util.Optional;

import edu.nd.crc.safa.server.entities.api.SafaError;

public interface VersionAction<VersionEntity> {

    Optional<VersionEntity> action() throws SafaError;
}
