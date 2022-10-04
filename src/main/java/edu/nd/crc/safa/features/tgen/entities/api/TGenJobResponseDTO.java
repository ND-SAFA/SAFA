package edu.nd.crc.safa.features.tgen.entities.api;

import lombok.Data;

/**
 * TGen response for creating a job with results outputted to a cloud file.
 */
@Data
public class TGenJobResponseDTO {
    /**
     * Path to file containing results of job.
     */
    private String jobID;
}
