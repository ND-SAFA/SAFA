package edu.nd.crc.safa.features.hgen;

import edu.nd.crc.safa.features.tgen.api.TGenDataset;
import edu.nd.crc.safa.features.tgen.api.responses.AbstractTGenResponse;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class TGenHGenResponse extends AbstractTGenResponse {
    /**
     * Generates artifacts for each cluster.
     */
    TGenDataset dataset;
}
