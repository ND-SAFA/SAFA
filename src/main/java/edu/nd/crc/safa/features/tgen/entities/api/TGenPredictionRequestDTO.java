package edu.nd.crc.safa.features.tgen.entities.api;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * The payload to the prediction endpoint of TGEN.
 */
@NoArgsConstructor
@AllArgsConstructor
@Data
public class TGenPredictionRequestDTO {
    /**
     * Path to model weights.
     */
    String model;
    /**
     * Dataset containing artifacts to predict trace links against.
     */
    TGenDataset dataset;
}
