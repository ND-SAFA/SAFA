package edu.nd.crc.safa.features.generation.common;

import java.util.List;
import javax.annotation.Nullable;

import edu.nd.crc.safa.features.jobs.logging.entities.JobLogEntry;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
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
    CeleryStatus status;
    /**
     * Message corresponding with status, used for reading error message.
     */
    String message;
    /**
     * The current logs of the job.
     */
    List<String> logs;
    /**
     * The current index of the log to read next.
     */
    @Nullable
    int currentLogIndex = 0;
    /**
     * The entry of the job.
     */
    @Nullable
    JobLogEntry jobLogEntry;

}
