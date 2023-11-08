package edu.nd.crc.safa.features.generation.common;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.features.jobs.logging.entities.JobLogEntry;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.annotation.Nullable;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Returns the status of TGEN task.
 */
@JsonIgnoreProperties(ignoreUnknown = true)
@Data
@NoArgsConstructor
public class TGenStatus {
    /**
     * The status of the celery job.
     */
    private CeleryStatus status;
    /**
     * Message corresponding with status, used for reading error message.
     */
    private String message;
    /**
     * The current logs of the job.
     */
    private List<String> logs = new ArrayList<>();
    /**
     * The current index of the log to read next.
     */
    @Nullable
    private int currentLogIndex = 0;
    /**
     * The entry of the job.
     */
    @Nullable
    private JobLogEntry jobLogEntry;

    public void update(TGenStatus status) {
        this.status = status.status;
        this.message = status.message;
        this.logs = status.logs;
        this.currentLogIndex = status.currentLogIndex > 0 ? status.currentLogIndex : this.currentLogIndex;
        this.jobLogEntry = status.jobLogEntry != null ? status.jobLogEntry : this.jobLogEntry;
    }
}
