package edu.nd.crc.safa.features.generation.common;

import java.util.UUID;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.annotation.Nullable;
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
    private UUID taskId;
    @Nullable
    private Class<T> responseClass;

    @Nullable
    private TGenStatus status;

    public void updateStatus(TGenStatus tGenStatus) {
        if (status == null) {
            this.status = tGenStatus;
        } else {
            this.status.update(tGenStatus);
        }
    }
}
