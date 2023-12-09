package edu.nd.crc.safa.features.flatfiles.builder.steps;

import java.io.IOException;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.builder.FlatFileBuilderStore;

public class UploadFilesStep implements IFlatFileBuilderStep {
    /**
     * Uploads files to project directory.
     *
     * @param store           The state of the flat file project builder.
     * @param serviceProvider Provide access to their services.
     * @throws IOException If error occurs while uploading files.
     */
    @Override
    public void perform(FlatFileBuilderStore store, ServiceProvider serviceProvider) throws IOException {
        serviceProvider.getFileUploadService().uploadFilesToServer(
            store.getProjectVersion().getProject(),
            store.getFiles());
    }
}
