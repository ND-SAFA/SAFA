package edu.nd.crc.safa.test.services;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.io.IOException;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.documents.entities.app.DocumentAppEntity;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.flatfiles.services.MultipartRequestService;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipAppEntity;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.requests.FlatFileRequest;
import edu.nd.crc.safa.test.requests.SafaRequest;
import edu.nd.crc.safa.test.services.builders.DbEntityBuilder;

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

    public ProjectVersion createProjectFromFiles(String projectName, String projectPath) throws Exception {
        ProjectVersion projectVersion = createProjectWithNewVersion(projectName);
        FlatFileRequest.updateProjectVersionFromFlatFiles(projectVersion, projectPath);
        return projectVersion;
    }

    public ProjectVersion uploadDefaultProject(String projectName) throws IOException {
        return uploadFilesToProject(
            projectName,
            ProjectPaths.Resources.Tests.DefaultProject.V1
        );
    }

    public ProjectVersion uploadFilesToProject(String projectName, String projectPath) throws IOException {
        ProjectVersion projectVersion = createProjectWithNewVersion(projectName);
        Project project = projectVersion.getProject();
        List<MultipartFile> files = MultipartRequestService.readDirectoryAsMultipartFiles(
            projectPath,
            "files");
        this.serviceProvider.getFileUploadService().uploadFilesToServer(project, files);
        return projectVersion;
    }

    public Pair<ProjectVersion, ProjectVersion> createDualVersions(String projectName) throws Exception {
        return createDualVersions(projectName, true);
    }

    public Pair<ProjectVersion, ProjectVersion> createDualVersions(String projectName, boolean uploadFiles)
        throws Exception {

        dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newVersion(projectName);

        ProjectVersion beforeVersion = dbEntityBuilder.getProjectVersion(projectName, 0);
        ProjectVersion afterVersion = dbEntityBuilder.getProjectVersion(projectName, 1);

        if (uploadFiles) {
            FlatFileRequest.updateProjectVersionFromFlatFiles(beforeVersion,
                ProjectPaths.Resources.Tests.DefaultProject.V1);
            FlatFileRequest.updateProjectVersionFromFlatFiles(afterVersion,
                ProjectPaths.Resources.Tests.DefaultProject.V2);
        }

        return new Pair<>(beforeVersion, afterVersion);
    }

    public JSONObject createOrUpdateDocument(ProjectVersion projectVersion,
                                             DocumentAppEntity documentAppEntity) throws Exception {
        JSONObject response =
            SafaRequest
                .withRoute(AppRoutes.Documents.CREATE_OR_UPDATE_DOCUMENT)
                .withVersion(projectVersion)
                .postWithJsonObject(documentAppEntity);

        UUID documentId = UUID.fromString(response.getString("documentId"));
        documentAppEntity.setDocumentId(documentId);
        return response;
    }

    public JSONObject createOrUpdateDocumentJson(ProjectVersion projectVersion,
                                                 Object docJson) throws Exception {
        return SafaRequest
            .withRoute(AppRoutes.Documents.CREATE_OR_UPDATE_DOCUMENT)
            .withVersion(projectVersion)
            .postWithJsonObject(docJson);

    }

    public JSONArray addArtifactToDocument(ProjectVersion projectVersion,
                                           Document document,
                                           Object artifactsJson) throws Exception {
        return SafaRequest
            .withRoute(AppRoutes.DocumentArtifact.ADD_ARTIFACTS_TO_DOCUMENT)
            .withVersion(projectVersion)
            .withDocument(document)
            .postWithJsonArray(artifactsJson);
    }

    public JSONObject shareProject(Project project,
                                   String email,
                                   ProjectRole role) throws Exception {
        return shareProject(project, email, role, status().is2xxSuccessful());
    }

    public JSONObject shareProject(Project project,
                                   String email,
                                   ProjectRole role,
                                   ResultMatcher resultMatcher) throws Exception {
        MembershipAppEntity request = new MembershipAppEntity(email, role.name());

        return SafaRequest
            .withRoute(AppRoutes.Memberships.BY_ENTITY_ID)
            .withEntityId(project.getProjectId())
            .postWithJsonObject(request, resultMatcher);
    }
}
