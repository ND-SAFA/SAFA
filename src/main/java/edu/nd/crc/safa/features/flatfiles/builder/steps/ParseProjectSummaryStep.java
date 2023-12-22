package edu.nd.crc.safa.features.flatfiles.builder.steps;

import java.io.File;
import java.nio.charset.StandardCharsets;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.builder.FlatFileBuilderStore;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.FileUtilities;

import org.apache.commons.io.FileUtils;

public class ParseProjectSummaryStep implements IFlatFileBuilderStep {
    private static final String SPECIFICATION_FILE_NAME = "project_summary.txt";

    /**
     * Adds project summary if file uploaded.
     *
     * @param state           The state of the flat file project builder.
     * @param serviceProvider Provide access to their services.
     * @throws Exception Exception if fail to read file.
     */
    @Override
    public void perform(FlatFileBuilderStore state, ServiceProvider serviceProvider) throws Exception {
        ProjectVersion projectVersion = state.getProjectVersion();
        String pathToFiles = ProjectPaths.Storage.projectUploadsPath(projectVersion.getProject(), false);
        String projectSummaryFilePath = FileUtilities.buildPath(pathToFiles, SPECIFICATION_FILE_NAME);
        File projectSummaryFile = new File(projectSummaryFilePath);
        if (projectSummaryFile.exists()) {
            String projectSummary = FileUtils.readFileToString(projectSummaryFile, StandardCharsets.UTF_8);
            Project project = state.getProjectVersion().getProject();
            project.setSpecification(projectSummary);
            serviceProvider.getProjectRepository().save(project);
            state.log("Specification is set.");
        } else {
            state.log("No project summary uploaded.");
        }
    }
}
