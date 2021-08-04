package unit.service;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;

import java.io.File;
import java.io.IOException;

import edu.nd.crc.safa.constants.ProjectPaths;
import edu.nd.crc.safa.entities.Project;
import edu.nd.crc.safa.entities.ProjectVersion;
import edu.nd.crc.safa.output.error.ServerError;
import edu.nd.crc.safa.services.FlatFileService;
import edu.nd.crc.safa.services.ProjectService;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.EntityBaseTest;

public class TestUploadFlatFiles extends EntityBaseTest {

    @Autowired
    FlatFileService flatFileService;

    @Autowired
    ProjectService projectService;

    @Test
    public void uploadTestResources() throws IOException, ServerError {
        String testProjectName = "testProject";
        ProjectVersion projectVersion = createProjectWithTestResources(testProjectName);
        Project project = projectVersion.getProject();

        //Cleanup
        this.projectVersionRepository.delete(projectVersion);
        projectService.deleteProject(project);
        File oldStorage = new File(ProjectPaths.getPathToStorage(project, false));
        assertThat(oldStorage.exists()).as("delete project storage").isFalse();
    }
}
