package unit.flatfile;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;

import java.io.File;
import java.io.IOException;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.flatfiles.services.FileUploadService;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.ApplicationBaseTest;

/**
 * Provides a smoke test for verifying that files can be uploaded and stored.
 */
public class TestUploadFiles extends ApplicationBaseTest {

    @Autowired
    FileUploadService fileUploadService;

    @Test
    public void uploadTestResources() throws IOException, SafaError {
        String testProjectName = "testProject";
        ProjectVersion projectVersion = createDefaultProject(testProjectName);
        Project project = projectVersion.getProject();

        //Cleanup
        this.projectVersionRepository.delete(projectVersion);
        projectService.deleteProject(project);
        File oldStorage = new File(ProjectPaths.getPathToUploadedFiles(project, false));
        assertThat(oldStorage.exists()).as("delete project storage").isFalse();
    }
}
