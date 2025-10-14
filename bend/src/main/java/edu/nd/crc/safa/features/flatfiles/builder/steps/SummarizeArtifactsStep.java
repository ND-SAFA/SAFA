package edu.nd.crc.safa.features.flatfiles.builder.steps;

import java.util.List;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.builder.FlatFileBuilderStore;
import edu.nd.crc.safa.features.generation.summary.SummaryService;

public class SummarizeArtifactsStep implements IFlatFileBuilderStep {
    /**
     * Summarizes the artifacts in project commit if summarization is turned on.
     *
     * @param state           The state of the flat file project builder.
     * @param serviceProvider Provide access to their services.
     * @throws Exception If error occurs while summarizing artifacts.
     */
    @Override
    public void perform(FlatFileBuilderStore state, ServiceProvider serviceProvider) throws Exception {
        if (!state.isSummarizeArtifacts()) {
            return;
        }
        ProjectCommitDefinition projectCommitDefinition = state.getProjectCommitDefinition();
        List<ArtifactAppEntity> newArtifacts = projectCommitDefinition.getArtifacts().getAdded();
        SummaryService summaryService = serviceProvider.getSummaryService();
        summaryService.addSummariesToCode(newArtifacts, null, state.getJobLogger());
        projectCommitDefinition.getArtifacts().setAdded(newArtifacts);
    }
}
