package edu.nd.crc.safa.features.billing.services;

import org.springframework.stereotype.Service;

@Service
public class CostEstimationService {

    /**
     * Estimates the cost of an hgen run
     *
     * @param numArtifacts The number of artifacts to generate off of
     * @param numLayers Number of layers to generate
     * @return The number of credits the run will use
     */
    public int estimateHgen(int numArtifacts, int numLayers) {
        return (int) Math.ceil(numArtifacts * (2 - (1 / Math.pow(2, numLayers))));
    }

}
