package edu.nd.crc.safa.server.entities.api;

import java.io.IOException;

/**
 * Defines an interface for lambdas that parse data files.
 */
public interface FileParser {
    void parseFile() throws SafaError, IOException;
}
