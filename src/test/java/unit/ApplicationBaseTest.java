package unit;

import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.Routes;
import edu.nd.crc.safa.server.entities.api.ServerError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.springframework.test.web.servlet.request.MockMultipartHttpServletRequestBuilder;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import org.springframework.web.multipart.MultipartFile;

/**
 * Provides the application specific operations to unit test.
 */
public class ApplicationBaseTest extends AuthenticatedBaseTest {

    public void uploadFlatFilesToVersion(ProjectVersion projectVersion,
                                         String pathToFileDir) throws Exception {
        assertTokenExists();
        String path = RouteBuilder
            .withRoute(Routes.updateProjectVersionFromFlatFiles)
            .withVersion(projectVersion)
            .get();
        MockMultipartHttpServletRequestBuilder beforeRequest = createMultiPartRequest(path,
            pathToFileDir);
        sendRequest(beforeRequest, MockMvcResultMatchers.status().isCreated(), this.token);
    }

    public ProjectVersion createProjectAndUploadBeforeFiles(String projectName) throws ServerError, IOException {
        ProjectVersion projectVersion = createProjectWithNewVersion(projectName);
        Project project = projectVersion.getProject();
        List<MultipartFile> files = MultipartHelper.createMultipartFilesFromDirectory(
            ProjectPaths.PATH_TO_BEFORE_FILES,
            "files");
        fileUploadService.uploadFilesToServer(project, files);
        return projectVersion;
    }

    public ProjectVersion createProjectWithNewVersion(String projectName) {
        return entityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .getProjectVersion(projectName, 0);
    }
}
