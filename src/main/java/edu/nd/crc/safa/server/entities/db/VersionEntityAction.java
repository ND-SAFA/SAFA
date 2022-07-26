package edu.nd.crc.safa.server.entities.db;

import java.util.Optional;

import edu.nd.crc.safa.server.entities.api.SafaError;

import com.fasterxml.jackson.core.JsonProcessingException;

/**
 * Represents a lambda returning a VersionEntity optional.
 *
 * @param <T> The type returned by the action.
 */
public interface VersionEntityAction<T> {

    Optional<T> action() throws SafaError, JsonProcessingException;
}
