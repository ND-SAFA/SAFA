package unit.service;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;

import java.io.File;
import java.io.IOException;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.api.ServerError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.services.FileUploadService;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.ApplicationBaseTest;

public class TestUploadFlatFiles extends ApplicationBaseTest {

    @Autowired
    FileUploadService fileUploadService;

    @Test
    public void uploadTestResources() throws IOException, ServerError {
        String testProjectName = "testProject";
        ProjectVersion projectVersion = createProjectAndUploadBeforeFiles(testProjectName);
        Project project = projectVersion.getProject();

        //Cleanup
        this.projectVersionRepository.delete(projectVersion);
        projectService.deleteProject(project);
        File oldStorage = new File(ProjectPaths.getPathToStorage(project, false));
        assertThat(oldStorage.exists()).as("delete project storage").isFalse();
    }
}
