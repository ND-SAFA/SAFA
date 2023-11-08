package edu.nd.crc.safa.features.flatfiles.builder.steps;

import java.io.IOException;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.builder.FlatFileBuilderArgs;

public class UploadFilesStep implements IFlatFileBuilderStep {
    @Override
    public void perform(FlatFileBuilderArgs state, ServiceProvider serviceProvider) throws IOException {
        serviceProvider.getFileUploadService().uploadFilesToServer(
            state.getProjectVersion().getProject(),
            state.getFiles());
    }
}
