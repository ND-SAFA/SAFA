package unit.utilities;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;

import java.nio.file.Files;
import java.nio.file.Paths;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.server.responses.ServerError;
import edu.nd.crc.safa.utilities.OSHelper;

import org.junit.jupiter.api.Test;
import unit.EntityBaseTest;

public class TestOSHelper extends EntityBaseTest {

    @Test
    public void smokeTest() throws ServerError {
        String testName = "hellWorld";
        Project project = entityBuilder.newProject(testName).getProject(testName);
        String pathToTestProject = ProjectPaths.getPathToStorage(project, false);

        assertThat(Files.exists(Paths.get(pathToTestProject))).as("dir not created").isFalse();
        OSHelper.clearOrCreateDirectory(pathToTestProject);
        assertThat(Files.exists(Paths.get(pathToTestProject))).as("dir is created").isTrue();

        OSHelper.deletePath(pathToTestProject);
        assertThat(Files.exists(Paths.get(pathToTestProject))).as("dir is cleaned up").isFalse();
    }
}
