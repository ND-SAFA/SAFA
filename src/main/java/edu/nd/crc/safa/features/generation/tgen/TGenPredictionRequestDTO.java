package edu.nd.crc.safa.features.generation.tgen;

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
    TGenDataset dataset;
}
