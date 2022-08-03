package edu.nd.crc.safa.features.flatfiles.entities;

import java.io.IOException;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;

/**
 * Defines an interface for lambdas that parse data files.
 */
public interface FileParser {
    void parseFile() throws SafaError, IOException;
}
