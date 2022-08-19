package services;

import java.io.IOException;
import java.util.List;

import requests.MultipartRequestService;
import requests.FlatFileRequest;
import requests.SafaRequest;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.memberships.entities.api.ProjectMembershipRequest;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.ProjectRole;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import builders.DbEntityBuilder;
import lombok.AllArgsConstructor;
import org.javatuples.Pair;
import org.json.JSONArray;
import org.json.JSONObject;
import org.springframework.test.web.servlet.ResultMatcher;
import org.springframework.web.multipart.MultipartFile;

@AllArgsConstructor
public class CreationTestService {
    ServiceProvider serviceProvider;
    DbEntityBuilder dbEntityBuilder;

    /**
     * Creates empty project with initial version.
     *
     * @param projectName The name of the project to create.
     * @return {@link ProjectVersion} initial project version (1.1.1);
     */
    public ProjectVersion createProjectWithNewVersion(String projectName) {
        return dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .getProjectVersion(projectName, 0);
    }

    public ProjectVersion createDefaultProject(String projectName) throws SafaError, IOException {
        ProjectVersion projectVersion = createProjectWithNewVersion(projectName);
        Project project = projectVersion.getProject();
        List<MultipartFile> files = MultipartRequestService.readDirectoryAsMultipartFiles(
            ProjectPaths.Tests.DefaultProject.V1,
            "files");
        this.serviceProvider.getFileUploadService().uploadFilesToServer(project, files);
        return projectVersion;
    }


    public Pair<ProjectVersion, ProjectVersion> createDualVersions(String projectName) throws Exception {
        return createDualVersions(projectName, true);
    }

    public Pair<ProjectVersion, ProjectVersion> createDualVersions(String projectName, boolean uploadFiles) throws Exception {
        dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newVersion(projectName);

        ProjectVersion beforeVersion = dbEntityBuilder.getProjectVersion(projectName, 0);
        ProjectVersion afterVersion = dbEntityBuilder.getProjectVersion(projectName, 1);

        if (uploadFiles) {
            FlatFileRequest.updateProjectVersionFromFlatFiles(beforeVersion,
                ProjectPaths.Tests.DefaultProject.V1);
            FlatFileRequest.updateProjectVersionFromFlatFiles(afterVersion, ProjectPaths.Tests.DefaultProject.V2);
        }

        return new Pair<>(beforeVersion, afterVersion);
    }

    public Pair<ProjectVersion, JSONObject> createProjectWithDocument(
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

    public JSONObject createOrUpdateDocumentJson(ProjectVersion projectVersion,
                                                 JSONObject docJson) throws Exception {
        return
            SafaRequest
                .withRoute(AppRoutes.Documents.CREATE_OR_UPDATE_DOCUMENT)
                .withVersion(projectVersion)
                .postWithJsonObject(docJson);
    }

    public JSONArray addArtifactToDocument(ProjectVersion projectVersion,
                                           Document document,
                                           JSONArray artifactsJson) throws Exception {
        return SafaRequest
            .withRoute(AppRoutes.DocumentArtifact.ADD_ARTIFACTS_TO_DOCUMENT)
            .withVersion(projectVersion)
            .withDocument(document)
            .postWithJsonArray(artifactsJson);
    }

    public JSONObject shareProject(Project project,
                                   String email,
                                   ProjectRole role,
                                   ResultMatcher resultMatcher) throws Exception {
        ProjectMembershipRequest request = new ProjectMembershipRequest(email, role);
        return SafaRequest
            .withRoute(AppRoutes.Projects.Membership.ADD_PROJECT_MEMBER)
            .withProject(project)
            .postWithJsonObject(request, resultMatcher);
    }
}
