package edu.nd.crc.safa.features.generation.common;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

/**
 * The base class for responses from TGEN regarding a job result.
 */
@JsonIgnoreProperties(ignoreUnknown = true)
public interface ITGenResponse {
    /**
     * The logs of the job result.
     *
     * @return The list of logs
     */
    List<String> getLogs();
}
