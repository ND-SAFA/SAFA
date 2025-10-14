package edu.nd.crc.safa.features.generation.tgen.entities;

/**
 * Supported trace generation algorithsm
 */
public enum TGenAlgorithms {
    VSM,
    GENERATION;

    /**
     * @return Returns the default trace algorithm.
     */
    public static TGenAlgorithms getDefaultAlgorithm() {
        return GENERATION;
    }
}
