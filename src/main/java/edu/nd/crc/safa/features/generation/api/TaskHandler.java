package edu.nd.crc.safa.features.generation.api;

import edu.nd.crc.safa.features.generation.common.TGenStatus;

interface TaskHandler {
    /**
     * Callable representing a callback after getting a new task status.
     *
     * @param task The new task status.
     */
    void handleTask(TGenStatus task);
}
