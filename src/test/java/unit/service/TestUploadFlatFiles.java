package unit.service;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;

import java.io.File;
import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.constants.ProjectPaths;
import edu.nd.crc.safa.entities.Project;
import edu.nd.crc.safa.output.error.ServerError;
import edu.nd.crc.safa.services.FlatFileService;
import edu.nd.crc.safa.services.ProjectService;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.multipart.MultipartFile;
import unit.entities.EntityBaseTest;
import unit.utilities.TestFileUtility;

public class TestUploadFlatFiles extends EntityBaseTest {

    @Autowired
    FlatFileService flatFileService;

    @Autowired
    ProjectService projectService;

    @Test
    public void uploadTestResources() throws IOException, ServerError {
        String testProjectName = "testProject";
        String attributeName = "files";
        Project project = createProject(testProjectName);
        System.out.println("PROJECTID:" + project.getProjectId());
        List<MultipartFile> files = TestFileUtility.createMultipartFilesFromDirectory(
            ProjectPaths.PATH_TO_TEST_RESOURCES,
            attributeName);
        List<String> uploadedFileNames = flatFileService.uploadFlatFiles(project, files);
        assertThat(uploadedFileNames.size()).isEqualTo(3);
        //Cleanup
        projectService.deleteProject(project);
        File oldStorage = new File(ProjectPaths.getPathToStorage(project, false));
        assertThat(oldStorage.exists()).as("delete project storage").isFalse();
    }
}
