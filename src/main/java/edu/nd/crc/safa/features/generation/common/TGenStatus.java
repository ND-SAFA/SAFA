package edu.nd.crc.safa.features.generation.common;

import java.util.List;

import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Returns the status of TGEN task.
 */
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


}
