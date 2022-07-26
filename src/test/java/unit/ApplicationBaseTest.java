package unit;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import edu.nd.crc.safa.builders.CommitBuilder;
import edu.nd.crc.safa.builders.MultipartRequestService;
import edu.nd.crc.safa.builders.requests.FlatFileRequest;
import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.api.ProjectMembershipRequest;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.Document;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectRole;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.services.retrieval.AppEntityRetrievalService;

import org.javatuples.Pair;
import org.json.JSONArray;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.test.web.servlet.ResultMatcher;
import org.springframework.web.multipart.MultipartFile;

/**
 * Testing layer for encapsulating application logic.
 */
public abstract class ApplicationBaseTest extends WebSocketBaseTest {

    @Autowired
    protected AppEntityRetrievalService appEntityRetrievalService;
    @Autowired
    UserDetailsService userDetailsService;

    public void setAuthorization() {
        UserDetails userDetails = userDetailsService.loadUserByUsername(defaultUser);
        UsernamePasswordAuthenticationToken authorization = new UsernamePasswordAuthenticationToken(
            userDetails,
            null,
            userDetails.getAuthorities());

        SecurityContextHolder.getContext().setAuthentication(authorization);
    }

    public ProjectAppEntity getProjectAtVersion(ProjectVersion projectVersion) {
        setAuthorization(); // Required because getting currentDocument requires a user be logged in
        return appEntityRetrievalService.retrieveProjectAppEntityAtProjectVersion(projectVersion);
    }

    public ProjectVersion createDefaultProject(String projectName) throws SafaError, IOException {
        ProjectVersion projectVersion = createProjectWithNewVersion(projectName);
        Project project = projectVersion.getProject();
        List<MultipartFile> files = MultipartRequestService.readDirectoryAsMultipartFiles(
            ProjectPaths.PATH_TO_DEFAULT_PROJECT,
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
        return SafaRequest
            .withRoute(AppRoutes.Projects.Commits.commitChange)
            .withVersion(commitVersion)
            .postWithJsonObject(commitBuilder.asJson(), expectedStatus);
    }

    protected Pair<ProjectVersion, ProjectVersion> createDualVersions(String projectName) throws Exception {
        return createDualVersions(projectName, true);
    }

    protected Pair<ProjectVersion, ProjectVersion> createDualVersions(String projectName, boolean uploadFiles) throws Exception {
        dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newVersion(projectName);

        ProjectVersion beforeVersion = dbEntityBuilder.getProjectVersion(projectName, 0);
        ProjectVersion afterVersion = dbEntityBuilder.getProjectVersion(projectName, 1);

        if (uploadFiles) {
            FlatFileRequest.updateProjectVersionFromFlatFiles(beforeVersion, ProjectPaths.PATH_TO_DEFAULT_PROJECT);
            FlatFileRequest.updateProjectVersionFromFlatFiles(afterVersion, ProjectPaths.PATH_TO_AFTER_FILES);
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
                                      ResultMatcher resultMatcher) throws Exception {
        ProjectMembershipRequest request = new ProjectMembershipRequest(email, role);
        return SafaRequest
            .withRoute(AppRoutes.Projects.Membership.addProjectMember)
            .withProject(project)
            .postWithJsonObject(toJson(request), resultMatcher);
    }

    protected JSONArray getProjectMembers(Project project) throws Exception {
        return SafaRequest
            .withRoute(AppRoutes.Projects.Membership.getProjectMembers)
            .withProject(project)
            .getWithJsonArray();
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

    protected JSONObject createOrUpdateDocumentJson(ProjectVersion projectVersion,
                                                    JSONObject docJson) throws Exception {
        return
            SafaRequest
                .withRoute(AppRoutes.Projects.Documents.createOrUpdateDocument)
                .withVersion(projectVersion)
                .postWithJsonObject(docJson);
    }

    protected JSONArray addArtifactToDocument(ProjectVersion projectVersion,
                                              Document document,
                                              JSONArray artifactsJson) throws Exception {
        return SafaRequest
            .withRoute(AppRoutes.Projects.DocumentArtifact.addArtifactsToDocument)
            .withVersion(projectVersion)
            .withDocument(document)
            .postWithJsonArray(artifactsJson);
    }

    protected String getArtifactId(List<ArtifactAppEntity> artifacts, String artifactName) {
        ArtifactAppEntity artifact =
            artifacts
                .stream()
                .filter(a -> a.name.equals(artifactName))
                .collect(Collectors.toList())
                .get(0);
        return artifact.getId();
    }

    private void assertArraysMatch(JSONArray expected, JSONArray actual) {
        assertThat(actual.length()).isEqualTo(expected.length());
        for (int i = 0; i < expected.length(); i++) {
            Object expectedValue = expected.get(i);
            Object actualValue = actual.get(i);
            assertMatch(expectedValue, actualValue);
        }
    }

    protected Pair<ProjectVersion, JSONObject> createProjectWithDocument(
        String projectName,
        JSONObject documentJson) throws Exception {
        // Step - Create empty project
        ProjectVersion projectVersion = dbEntityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);

        // Step - Send creation request.
        JSONObject docCreated = createOrUpdateDocumentJson(projectVersion, documentJson);

        return new Pair<>(projectVersion, docCreated);
    }
}
