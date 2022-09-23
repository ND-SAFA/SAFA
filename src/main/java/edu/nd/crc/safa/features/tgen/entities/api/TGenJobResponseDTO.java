package edu.nd.crc.safa.features.tgen.entities.api;

import lombok.Getter;

/**
 * TGen response for creating a job with results outputted to a cloud file.
 */
public class TGenJobResponseDTO {
    /**
     * Path to file containing results of job.
     */
    @Getter
    private String outputPath;

    public void setOutputPath(String outputPath) {
        this.outputPath = outputPath.contains("/gcp") ? outputPath.replace("/gcp/", "") : outputPath;
    }
}
