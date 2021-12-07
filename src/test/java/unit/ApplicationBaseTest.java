package unit;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.builders.CommitBuilder;
import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.services.ProjectRetrievalService;

import org.javatuples.Pair;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.web.servlet.request.MockMultipartHttpServletRequestBuilder;
import org.springframework.web.multipart.MultipartFile;

/**
 * Testing layer for encapsulating application logic.
 */
public class ApplicationBaseTest extends AuthenticatedBaseTest {

    @Autowired
    protected ProjectRetrievalService projectRetrievalService;

    public void uploadFlatFilesToVersion(ProjectVersion projectVersion,
                                         String pathToFileDir) throws Exception {
        assertTokenExists();
        String path = RouteBuilder
            .withRoute(AppRoutes.Projects.updateProjectVersionFromFlatFiles)
            .withVersion(projectVersion)
            .get();
        MockMultipartHttpServletRequestBuilder beforeRequest = createMultiPartRequest(path,
            pathToFileDir);
        sendRequest(beforeRequest, status().isCreated(), this.token);
    }

    public ProjectVersion createProjectAndUploadBeforeFiles(String projectName) throws SafaError, IOException {
        ProjectVersion projectVersion = createProjectWithNewVersion(projectName);
        Project project = projectVersion.getProject();
        List<MultipartFile> files = MultipartHelper.createMultipartFilesFromDirectory(
            ProjectPaths.PATH_TO_BEFORE_FILES,
            "files");
        fileUploadService.uploadFilesToServer(project, files);
        return projectVersion;
    }

    public ProjectVersion createProjectWithNewVersion(String projectName) {
        return dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .getProjectVersion(projectName, 0);
    }

    public void commit(CommitBuilder commitBuilder) throws Exception {
        ProjectVersion commitVersion = commitBuilder.get().getCommitVersion();
        String route = RouteBuilder
            .withRoute(AppRoutes.Projects.commitChange)
            .withVersion(commitVersion)
            .get();
        sendPost(route, commitBuilder.asJson(), status().is2xxSuccessful());
    }

    /**
     * Returns the route for committing changes to project versions.
     *
     * @param projectVersion The base version to commit to.
     * @return The route to the endpoint.
     */
    protected String getCommitRoute(ProjectVersion projectVersion) {
        return RouteBuilder
            .withRoute(AppRoutes.Projects.commitChange)
            .withVersion(projectVersion)
            .get();
    }

    protected Pair<ProjectVersion, ProjectVersion> setupDualVersions(String projectName) throws Exception {
        return setupDualVersions(projectName, true);
    }

    protected Pair<ProjectVersion, ProjectVersion> setupDualVersions(String projectName, boolean uploadFiles) throws Exception {
        dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newVersion(projectName);

        ProjectVersion beforeVersion = dbEntityBuilder.getProjectVersion(projectName, 0);
        ProjectVersion afterVersion = dbEntityBuilder.getProjectVersion(projectName, 1);

        if (uploadFiles) {
            uploadFlatFilesToVersion(beforeVersion, ProjectPaths.PATH_TO_BEFORE_FILES);
            uploadFlatFilesToVersion(afterVersion, ProjectPaths.PATH_TO_AFTER_FILES);
        }

        return new Pair<>(beforeVersion, afterVersion);
    }
}
