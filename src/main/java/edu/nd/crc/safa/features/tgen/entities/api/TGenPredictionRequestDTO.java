package edu.nd.crc.safa.features.tgen.entities.api;

import javax.annotation.Nullable;

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
    /**
     * The prompt to use to determine if two artifacts are traced.
     */
    @Nullable
    String prompt;

    public TGenPredictionRequestDTO(String model, TGenDataset dataset) {
        this.model = model;
        this.dataset = dataset;
    }
}
