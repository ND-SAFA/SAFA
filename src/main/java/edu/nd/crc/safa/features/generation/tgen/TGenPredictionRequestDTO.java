package edu.nd.crc.safa.features.generation.tgen;

import edu.nd.crc.safa.features.generation.common.GenerationDataset;

import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * The payload to the prediction endpoint of TGEN.
 */
@AllArgsConstructor
@Data
public class TGenPredictionRequestDTO {
    /**
     * Dataset containing artifacts to predict trace links against.
     */
    GenerationDataset dataset;
}
