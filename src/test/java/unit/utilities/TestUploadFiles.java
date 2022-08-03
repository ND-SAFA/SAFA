package unit.utilities;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;

import java.nio.file.Files;
import java.nio.file.Paths;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.utilities.OSHelper;

import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

/**
 * Test that user is able to create new directory and upload files.
 */
class TestUploadFiles extends ApplicationBaseTest {

    @Test
    void smokeTest() throws SafaError {
        String testName = "hellWorld";
        Project project = dbEntityBuilder.newProject(testName).getProject(testName);
        String pathToTestProject = ProjectPaths.getPathToUploadedFiles(project, false);

        assertThat(Files.exists(Paths.get(pathToTestProject))).as("dir not created").isFalse();
        OSHelper.clearOrCreateDirectory(pathToTestProject);
        assertThat(Files.exists(Paths.get(pathToTestProject))).as("dir is created").isTrue();

        OSHelper.deletePath(pathToTestProject);
        assertThat(Files.exists(Paths.get(pathToTestProject))).as("dir is cleaned up").isFalse();
    }
}
