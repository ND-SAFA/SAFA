package edu.nd.crc.safa.features.generation.common;

import java.util.UUID;
import javax.annotation.Nullable;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Task identifier response.
 */
@JsonIgnoreProperties(ignoreUnknown = true)
@Data
@NoArgsConstructor
public class TGenTask<T> {
    /**
     * UUID for task subitted to TGEN.
     */
    @JsonProperty("task_id")
    UUID taskId;
    @Nullable
    Class<T> responseClass;

}
