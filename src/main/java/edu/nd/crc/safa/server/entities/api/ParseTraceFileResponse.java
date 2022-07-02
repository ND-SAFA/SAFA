package edu.nd.crc.safa.server.entities.api;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;

import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * The response object for parsing traces containing the traces themselves
 * and any errors that occurred during process.
 */
@NoArgsConstructor
@Data
public class ParseTraceFileResponse implements ParseFileResponse {

    List<TraceAppEntity> traces = new ArrayList<>();
    List<String> errors = new ArrayList<>();
}
