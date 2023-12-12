package edu.nd.crc.safa.features.flatfiles.builder.steps;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.builder.FlatFileBuilderStore;
import edu.nd.crc.safa.features.flatfiles.parser.FlatFileParser;
import edu.nd.crc.safa.features.flatfiles.parser.TimFileParser;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.JsonFileUtilities;

import org.json.JSONObject;

public class ParsingSetupStep implements IFlatFileBuilderStep {
    @Override
    public void perform(FlatFileBuilderStore state, ServiceProvider serviceProvider) throws Exception {
        Project project = state.getProjectVersion().getProject();

        JSONObject timFileJson = getTimFileContent(project);
        ProjectVersion projectVersion = state.getProjectVersion();

        String pathToFiles = ProjectPaths.Storage.projectUploadsPath(projectVersion.getProject(), false);
        state.setTimFileParser(new TimFileParser(timFileJson, pathToFiles));
        state.setFlatFileParser(new FlatFileParser(state.getTimFileParser()));
        state.setTimFileJson(timFileJson);
    }

    public JSONObject getTimFileContent(Project project) throws IOException {
        String pathToTimFile = ProjectPaths.Storage.uploadedProjectFilePath(project, ProjectVariables.TIM_FILENAME);
        if (!Files.exists(Paths.get(pathToTimFile))) {
            throw new SafaError("TIM.json file was not uploaded for this project");
        }
        return JsonFileUtilities.readJSONFile(pathToTimFile);
    }
}
