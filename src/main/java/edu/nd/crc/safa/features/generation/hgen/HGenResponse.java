package edu.nd.crc.safa.features.generation.hgen;

import java.util.List;

import edu.nd.crc.safa.features.generation.common.GenerationDataset;
import edu.nd.crc.safa.features.generation.common.ITGenResponse;

import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * The response from HGEN endpoint.
 */
@Data
@NoArgsConstructor
public class HGenResponse extends GenerationDataset implements ITGenResponse {
    /**
     * The logs occurring during job execution.
     */
    List<String> logs;
}
