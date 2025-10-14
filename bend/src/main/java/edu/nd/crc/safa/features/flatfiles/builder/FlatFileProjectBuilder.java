package edu.nd.crc.safa.features.flatfiles.builder;

import java.util.List;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.builder.steps.CommitStep;
import edu.nd.crc.safa.features.flatfiles.builder.steps.GenerateTraceLinksStep;
import edu.nd.crc.safa.features.flatfiles.builder.steps.IFlatFileBuilderStep;
import edu.nd.crc.safa.features.flatfiles.builder.steps.ParseArtifactStep;
import edu.nd.crc.safa.features.flatfiles.builder.steps.ParseProjectSummaryStep;
import edu.nd.crc.safa.features.flatfiles.builder.steps.ParseTraces;
import edu.nd.crc.safa.features.flatfiles.builder.steps.ParsingSetupStep;
import edu.nd.crc.safa.features.flatfiles.builder.steps.SummarizeArtifactsStep;
import edu.nd.crc.safa.features.flatfiles.builder.steps.UploadFilesStep;

import lombok.AccessLevel;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Builder project from flat files.
 */
@NoArgsConstructor(access = AccessLevel.PRIVATE)
@Data
public class FlatFileProjectBuilder {
    private static final List<IFlatFileBuilderStep> STEPS = List.of(
        new UploadFilesStep(),
        new ParsingSetupStep(),
        new ParseProjectSummaryStep(),
        new ParseArtifactStep(),
        new ParseTraces(),
        new SummarizeArtifactsStep(),
        new GenerateTraceLinksStep(),
        new CommitStep()
    );

    /**
     * Parses flat files and commits project to project version.
     *
     * @param store           State containing all configuration information about the upload.
     * @param serviceProvider Provides access to the services to fetch and commit data.
     */
    public static void build(FlatFileBuilderStore store, ServiceProvider serviceProvider) {
        for (IFlatFileBuilderStep step : STEPS) {
            try {
                step.perform(store, serviceProvider);
            } catch (Exception e) {
                e.printStackTrace();
                String error = String.format("Unable to complete step (%s) due to error:\n\n%s",
                    step.getClass().getSimpleName(),
                    e.getMessage());
                throw new RuntimeException(error);
            }
        }
    }
}
