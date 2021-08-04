package unit.utilities;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;

import java.nio.file.Files;
import java.nio.file.Paths;

import edu.nd.crc.safa.constants.ProjectPaths;
import edu.nd.crc.safa.entities.Project;
import edu.nd.crc.safa.output.error.ServerError;
import edu.nd.crc.safa.utilities.OSHelper;

import org.junit.jupiter.api.Test;
import unit.entities.EntityBaseTest;

public class TestOSHelper extends EntityBaseTest {

    @Test
    public void smokeTest() throws ServerError {
        String testName = "hellWorld";
        Project project = createProject(testName);
        String pathToTestProject = ProjectPaths.getPathToStorage(project, false);

        assertThat(Files.exists(Paths.get(pathToTestProject))).as("dir not created").isFalse();
        OSHelper.clearOrCreateDirectory(pathToTestProject);
        assertThat(Files.exists(Paths.get(pathToTestProject))).as("dir is created").isTrue();

        OSHelper.deletePath(pathToTestProject);
        assertThat(Files.exists(Paths.get(pathToTestProject))).as("dir is cleaned up").isFalse();
    }
}
