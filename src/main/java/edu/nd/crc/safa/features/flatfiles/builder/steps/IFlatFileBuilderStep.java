package edu.nd.crc.safa.features.flatfiles.builder.steps;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.builder.FlatFileBuilderArgs;

/**
 * Performs step in building project from flat files.
 */
public interface IFlatFileBuilderStep {

    /**
     * Performs step on flat file builder.
     *
     * @param serviceProvider Provide access to their services.
     */
    void perform(FlatFileBuilderArgs state, ServiceProvider serviceProvider) throws Exception;
}
