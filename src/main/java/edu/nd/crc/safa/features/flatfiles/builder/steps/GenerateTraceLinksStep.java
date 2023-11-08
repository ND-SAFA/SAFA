package edu.nd.crc.safa.features.flatfiles.builder.steps;

import java.util.List;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.builder.FlatFileBuilderArgs;
import edu.nd.crc.safa.features.flatfiles.parser.FlatFileParser;
import edu.nd.crc.safa.features.generation.tgen.entities.TGenRequestAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

public class GenerateTraceLinksStep implements IFlatFileBuilderStep {
    @Override
    public void perform(FlatFileBuilderArgs state, ServiceProvider serviceProvider) throws Exception {
        ProjectAppEntity projectAppEntity = new ProjectAppEntity();
        ProjectCommitDefinition commit = state.getProjectCommitDefinition();

        List<TraceAppEntity> manualLinks = commit.getTraces().getAdded();

        projectAppEntity.setArtifacts(commit.getArtifacts().getAdded());
        projectAppEntity.setTraces(manualLinks);

        FlatFileParser flatFileParser = state.getFlatFileParser();

        TGenRequestAppEntity tgenRequest = flatFileParser.getTGenRequestAppEntity();
        List<TraceAppEntity> generatedTraces =
            serviceProvider.getTraceGenerationService().generateTraceLinks(tgenRequest, projectAppEntity);

        generatedTraces = serviceProvider
            .getTraceGenerationService()
            .removeOverlappingLinks(manualLinks, generatedTraces);
        commit.getTraces().getAdded().addAll(generatedTraces);
    }
}
