package edu.nd.crc.safa.utilities;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;

/**
 * No input or output function that might throw {@link Exception}
 */
@FunctionalInterface
public interface ExecutorTask {

    void run() throws SafaError;
}
