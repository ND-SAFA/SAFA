package edu.nd.crc.safa.features.flatfiles.builder.steps;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.builder.FlatFileBuilderStore;

/**
 * Performs step in building project from flat files.
 */
public interface IFlatFileBuilderStep {

    /**
     * Performs step on flat file builder.
     *
     * @param state           The state of the flat file project builder.
     * @param serviceProvider Provide access to their services.
     */
    void perform(FlatFileBuilderStore state, ServiceProvider serviceProvider) throws Exception;
}
