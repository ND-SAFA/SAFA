package edu.nd.crc.safa.features.projects.entities.app;

import java.io.IOException;

/**
 * Defines a lambda for creating a generic object from a string;
 *
 * @param <O> The type of object that is created.
 */
public interface StringCreator<O> {
    O create(String content) throws IOException;
}
