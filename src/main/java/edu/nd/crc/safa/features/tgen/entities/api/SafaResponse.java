package edu.nd.crc.safa.features.tgen.entities.api;

import java.util.UUID;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * The generic response from TGEN.
 */
@Data
@NoArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class SafaResponse<T> {
    /**
     * ID of job performed.
     */
    @JsonProperty("job_id")
    UUID jobId;
    /**
     * -1 if failure, 0 is success.
     */
    int status;
    /**
     * Generic body of request.
     */
    T body;
}
