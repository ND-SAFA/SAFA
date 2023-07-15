package edu.nd.crc.safa.features.generation.common;

import java.util.List;

/**
 * The base class for responses from TGEN regarding a job result.
 */
public interface ITGenResponse {
    /**
     * The logs of the job result.
     */
    List<String> getLogs();
}
