package unit.service;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;

import java.io.File;
import java.io.IOException;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.responses.ServerError;
import edu.nd.crc.safa.server.services.FlatFileService;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.EntityBaseTest;

public class TestUploadFlatFiles extends EntityBaseTest {

    @Autowired
    FlatFileService flatFileService;

    @Test
    public void uploadTestResources() throws IOException, ServerError {
        String testProjectName = "testProject";
        ProjectVersion projectVersion = createProjectUploadedResources(testProjectName);
        Project project = projectVersion.getProject();

        //Cleanup
        this.projectVersionRepository.delete(projectVersion);
        projectService.deleteProject(project);
        File oldStorage = new File(ProjectPaths.getPathToStorage(project, false));
        assertThat(oldStorage.exists()).as("delete project storage").isFalse();
    }
}
