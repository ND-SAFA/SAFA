package edu.nd.crc.safa.features.hgen;

import edu.nd.crc.safa.features.tgen.api.TGenDataset;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class TGenHGenResponse {
    /**
     * Generates artifacts for each cluster.
     */
    TGenDataset dataset;
}
