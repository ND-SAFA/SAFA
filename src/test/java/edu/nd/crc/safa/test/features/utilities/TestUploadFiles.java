package edu.nd.crc.safa.test.features.utilities;

import static org.assertj.core.api.Assertions.assertThat;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.utilities.FileUtilities;

import org.junit.jupiter.api.Test;

/**
 * Test that user is able to create new directory and upload files.
 */
class TestUploadFiles extends ApplicationBaseTest {

    @Test
    void smokeTest() throws SafaError, IOException {
        String testName = "hellWorld";
        Project project = dbEntityBuilder.newProject(testName).getProject(testName);
        String pathToTestProject = ProjectPaths.Storage.projectUploadsPath(project, false);

        assertThat(Files.exists(Paths.get(pathToTestProject))).as("dir not created").isFalse();
        FileUtilities.clearOrCreateDirectory(pathToTestProject);
        assertThat(Files.exists(Paths.get(pathToTestProject))).as("dir is created").isTrue();

        FileUtilities.deletePath(pathToTestProject);
        assertThat(Files.exists(Paths.get(pathToTestProject))).as("dir is cleaned up").isFalse();
    }
}
