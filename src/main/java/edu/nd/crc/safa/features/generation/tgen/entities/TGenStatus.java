package edu.nd.crc.safa.features.generation.tgen.entities;

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
     * -1 = Failure
     * 0 = Success
     * 1 = Not Started
     * 2 = In Progress
     */
    int status;
    /**
     * Message corresponding with status, used for reading error message.
     */
    String message;
    /**
     * The current logs of the job.
     */
    List<String> logs;
}
