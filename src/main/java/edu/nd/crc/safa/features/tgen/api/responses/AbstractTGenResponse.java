package edu.nd.crc.safa.features.tgen.api.responses;

import java.util.List;

import lombok.Data;

/**
 * The base class for responses from TGEN regarding a job result.
 */
@Data
public class AbstractTGenResponse {
    /**
     * The logs of the job result.
     */
    List<String> logs;
}
