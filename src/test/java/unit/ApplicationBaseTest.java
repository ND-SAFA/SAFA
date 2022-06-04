package unit;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.builders.CommitBuilder;
import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.common.AppRoutes;
import edu.nd.crc.safa.common.ProjectPaths;
import edu.nd.crc.safa.server.entities.api.ProjectMembershipRequest;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectRole;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.services.retrieval.AppEntityRetrievalService;

import org.javatuples.Pair;
import org.json.JSONArray;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.web.servlet.ResultMatcher;
import org.springframework.test.web.servlet.request.MockMultipartHttpServletRequestBuilder;
import org.springframework.web.multipart.MultipartFile;

/**
 * Testing layer for encapsulating application logic.
 */
public class ApplicationBaseTest extends WebSocketBaseTest {

    @Autowired
    protected AppEntityRetrievalService appEntityRetrievalService;

    public void uploadFlatFilesToVersion(ProjectVersion projectVersion,
                                         String pathToFileDir) throws Exception {
        uploadFlatFilesToVersion(projectVersion,
            pathToFileDir,
            AppRoutes.Projects.FlatFiles.updateProjectVersionFromFlatFiles);
    }

    public JSONObject uploadFlatFilesToVersion(ProjectVersion projectVersion,
                                               String pathToFileDir,
                                               String baseRoute) throws Exception {
        assertTokenExists();
        String path = RouteBuilder
            .withRoute(baseRoute)
            .withVersion(projectVersion)
            .get();
        MockMultipartHttpServletRequestBuilder beforeRequest = createMultiPartRequest(path,
            pathToFileDir);
        return sendRequest(beforeRequest, status().isCreated(), this.token);
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

    public JSONObject commit(CommitBuilder commitBuilder) throws Exception {
        return commitWithStatus(commitBuilder, status().is2xxSuccessful());
    }

    public JSONObject commitWithStatus(CommitBuilder commitBuilder, ResultMatcher expectedStatus) throws Exception {
        ProjectVersion commitVersion = commitBuilder.get().getCommitVersion();
        String route = RouteBuilder
            .withRoute(AppRoutes.Projects.Commits.commitChange)
            .withVersion(commitVersion)
            .get();
        return sendPost(route, commitBuilder.asJson(), expectedStatus);
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

    public String getId(String projectName, String artifactName) {
        Project project = this.dbEntityBuilder.getProject(projectName);
        Optional<Artifact> artifactOptional = this.artifactRepository.findByProjectAndName(project, artifactName);
        if (artifactOptional.isPresent()) {
            return artifactOptional.get().getArtifactId().toString();
        }
        throw new RuntimeException("Could not find artifact with name:" + artifactName);
    }

    protected JSONObject shareProject(Project project,
                                      String email,
                                      ProjectRole role,
                                      ResultMatcher httpResult) throws Exception {
        ProjectMembershipRequest request = new ProjectMembershipRequest(email, role);
        String url = RouteBuilder.withRoute(AppRoutes.Projects.Membership.addProjectMember).withProject(project).get();
        return sendPost(url, toJson(request), httpResult);
    }

    protected JSONArray getProjectMembers(Project project) throws Exception {
        String url = RouteBuilder
            .withRoute(AppRoutes.Projects.Membership.getProjectMembers)
            .withProject(project)
            .get();
        return sendGetWithArrayResponse(url, status().is2xxSuccessful());
    }

    protected void assertMatch(Object expected, Object actual) {
        if (expected instanceof JSONObject) {
            assertObjectsMatch((JSONObject) expected, (JSONObject) actual);
        } else if (expected instanceof JSONArray) {
            assertArraysMatch((JSONArray) expected, (JSONArray) actual);
        } else {
            assertThat(actual).isEqualTo(expected);
        }
    }

    protected void assertObjectsMatch(JSONObject expected, JSONObject actual) {
        assertObjectsMatch(expected, actual, new ArrayList<>());
    }

    protected void assertObjectsMatch(JSONObject expected,
                                      JSONObject actual,
                                      List<String> ignoreProperties) {
        for (Iterator<String> expectedIterator = expected.keys(); expectedIterator.hasNext(); ) {
            String key = expectedIterator.next();
            if (ignoreProperties.contains(key)) {
                continue;
            }

            if (!actual.has(key)) {
                throw new RuntimeException(actual + " does not contain key:" + key);
            }

            Object expectedValue = expected.get(key);
            Object actualValue = actual.get(key);

            assertMatch(expectedValue, actualValue);
        }
    }

    protected JSONObject createOrUpdateDocumentJson(ProjectVersion projectVersion, JSONObject docJson) throws Exception {
        String route =
            RouteBuilder
                .withRoute(AppRoutes.Projects.Documents.createOrUpdateDocument)
                .withVersion(projectVersion)
                .get();
        return sendPost(route, docJson, status().isCreated());
    }

    private void assertArraysMatch(JSONArray expected, JSONArray actual) {
        assertThat(actual.length()).isEqualTo(expected.length());
        for (int i = 0; i < expected.length(); i++) {
            Object expectedValue = expected.get(i);
            Object actualValue = actual.get(i);
            assertMatch(expectedValue, actualValue);
        }
    }
}
