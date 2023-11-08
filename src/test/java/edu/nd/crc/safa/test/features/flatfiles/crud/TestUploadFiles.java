package edu.nd.crc.safa.test.features.flatfiles.crud;

import static org.assertj.core.api.Assertions.assertThat;

import java.io.File;
import java.io.IOException;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.flatfiles.services.FileUploadService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Provides a smoke test for verifying that files can be uploaded and stored.
 */
class TestUploadFiles extends ApplicationBaseTest {

    @Autowired
    FileUploadService fileUploadService;

    @Test
    void uploadTestResources() throws IOException, SafaError {
        String testProjectName = "testProject";
        ProjectVersion projectVersion = creationService.uploadDefaultProject(testProjectName);
        Project project = projectVersion.getProject();

        //Cleanup
        this.projectVersionRepository.delete(projectVersion);
        projectService.deleteProject(getCurrentUser(), project);
        File oldStorage = new File(ProjectPaths.Storage.projectUploadsPath(project, false));
        assertThat(oldStorage).as("delete project storage").doesNotExist();
    }
}
