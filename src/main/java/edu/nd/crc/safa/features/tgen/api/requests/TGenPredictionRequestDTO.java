package edu.nd.crc.safa.features.tgen.api.requests;

import javax.annotation.Nullable;

import edu.nd.crc.safa.features.tgen.api.TGenDataset;

import lombok.Data;

/**
 * The payload to the prediction endpoint of TGEN.
 */
@Data
public class TGenPredictionRequestDTO {
    /**
     * Dataset containing artifacts to predict trace links against.
     */
    TGenDataset dataset;
    /**
     * The prompt to use to determine if two artifacts are traced.
     */
    @Nullable
    String prompt;

    public TGenPredictionRequestDTO(TGenDataset dataset, String prompt) {
        this.dataset = dataset;
        this.prompt = prompt;
    }
}
