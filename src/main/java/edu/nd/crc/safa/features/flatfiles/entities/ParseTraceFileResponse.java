package edu.nd.crc.safa.features.flatfiles.entities;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

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
