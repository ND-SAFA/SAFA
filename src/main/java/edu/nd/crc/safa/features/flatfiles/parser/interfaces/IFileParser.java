package edu.nd.crc.safa.features.flatfiles.parser.interfaces;

import java.io.IOException;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;

/**
 * Defines an interface for lambdas that parse data files.
 */
public interface IFileParser {
    void parseFile() throws SafaError, IOException;
}
