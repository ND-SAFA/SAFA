package edu.nd.crc.safa.server.entities.db;

import java.util.Optional;

import edu.nd.crc.safa.server.entities.api.SafaError;

/**
 * Represents a lambda returning a VersionEntity optional.
 *
 * @param <VersionEntity>
 */
public interface VersionEntityAction<VersionEntity> {

    Optional<VersionEntity> action() throws SafaError;
}
