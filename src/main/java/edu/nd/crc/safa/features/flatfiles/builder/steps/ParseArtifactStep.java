package edu.nd.crc.safa.features.flatfiles.builder.steps;

import java.util.List;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.EntityParsingResult;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.builder.BuilderUtility;
import edu.nd.crc.safa.features.flatfiles.builder.FlatFileBuilderStore;
import edu.nd.crc.safa.features.flatfiles.parser.FlatFileParser;
import edu.nd.crc.safa.features.flatfiles.parser.TimFileParser;
import edu.nd.crc.safa.features.projects.entities.db.ProjectEntityType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.json.JSONObject;

public class ParseArtifactStep implements IFlatFileBuilderStep {
    @Override
    public void perform(FlatFileBuilderStore state, ServiceProvider serviceProvider) throws Exception {
        ProjectVersion projectVersion = state.getProjectVersion();
        ProjectCommitDefinition projectCommitDefinition = state.getProjectCommitDefinition();

        // Step - Read Tim.
        JSONObject timFileJson = state.getTimFileJson();

        // Step - Create project parser
        String pathToFiles = ProjectPaths.Storage.projectUploadsPath(projectVersion.getProject(), false);
        TimFileParser timFileParser = new TimFileParser(timFileJson, pathToFiles);
        FlatFileParser flatFileParser = new FlatFileParser(timFileParser);

        // Step - parse artifacts
        EntityParsingResult<ArtifactAppEntity, String> artifactCreationResponse = flatFileParser.parseArtifacts();
        List<ArtifactAppEntity> artifactsAdded = artifactCreationResponse.getEntities();
        for (ArtifactAppEntity artifact : artifactsAdded) {
            serviceProvider.getArtifactRepository().findByProjectIdAndName(projectVersion.getProject().getId(),
                artifact.getName()).ifPresent(a -> artifact.setId(a.getArtifactId()));
        }
        projectCommitDefinition.getArtifacts().setAdded(artifactCreationResponse.getEntities());
        BuilderUtility.addErrorsToCommit(projectCommitDefinition,
            artifactCreationResponse.getErrors(),
            ProjectEntityType.ARTIFACTS);

        state.setArtifactsAdded(artifactsAdded);
    }
}
