package edu.nd.crc.safa.server.entities.api;

/**
 * Defines an interface for lambdas that parse data files.
 */
public interface FileParser {
    void parseFile() throws ServerError;
}
