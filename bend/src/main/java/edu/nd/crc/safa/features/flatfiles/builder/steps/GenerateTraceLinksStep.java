package edu.nd.crc.safa.features.flatfiles.builder.steps;

import java.util.List;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.builder.FlatFileBuilderStore;
import edu.nd.crc.safa.features.flatfiles.parser.FlatFileParser;
import edu.nd.crc.safa.features.generation.tgen.entities.TGenRequestAppEntity;
import edu.nd.crc.safa.features.permissions.checks.billing.HasUnlimitedCreditsCheck;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.permissions.services.PermissionService;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

public class GenerateTraceLinksStep implements IFlatFileBuilderStep {
    @Override
    public void perform(FlatFileBuilderStore state, ServiceProvider serviceProvider) throws Exception {
        FlatFileParser flatFileParser = state.getFlatFileParser();
        TGenRequestAppEntity tgenRequest = flatFileParser.getTGenRequestAppEntity();

        if (tgenRequest.size() > 0) {
            PermissionService permissionService = serviceProvider.getPermissionService();
            ProjectVersion projectVersion = state.getProjectVersion();

            permissionService.requirePermission(ProjectPermission.GENERATE, projectVersion, state.getUser());
            permissionService.requireAdditionalCheck(new HasUnlimitedCreditsCheck(), projectVersion, state.getUser());
        }
        ProjectAppEntity projectAppEntity = new ProjectAppEntity();
        ProjectCommitDefinition commit = state.getProjectCommitDefinition();

        List<TraceAppEntity> manualLinks = commit.getTraces().getAdded();

        projectAppEntity.setArtifacts(commit.getArtifacts().getAdded());
        projectAppEntity.setTraces(manualLinks);


        List<TraceAppEntity> generatedTraces =
            serviceProvider.getTraceGenerationService().generateTraceLinks(tgenRequest, projectAppEntity);

        generatedTraces = serviceProvider
            .getTraceGenerationService()
            .removeOverlappingLinks(manualLinks, generatedTraces);
        commit.getTraces().getAdded().addAll(generatedTraces);
    }
}
