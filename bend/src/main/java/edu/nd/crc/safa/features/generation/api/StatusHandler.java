package edu.nd.crc.safa.features.generation.api;

interface StatusHandler {
    /**
     * Callable representing a call to get the status of a job.
     *
     * @return True if job is done false otherwise.
     */
    boolean statusHandler();
}
