package edu.nd.crc.safa.test.features.projects.download;

import static org.assertj.core.api.Assertions.assertThat;

import java.io.File;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.authentication.AuthorizationSetter;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.flatfiles.services.DataFileBuilder;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.builders.ProjectBuilder;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Creates a project containing one of each type of artifact and attempts to download and
 * re-upload the project.
 */
class TestDownloadAndReuploadFlatFiles extends ApplicationBaseTest {
    String projectName = "first-project";

    @Test
    void downloadAndReuploadFlatFiles() throws Exception {
        AuthorizationSetter.setSessionAuthorization(defaultUser, this.serviceProvider);
        // Step - Create project with artifacts from docs: artifact tree, safety case, fta
        ProjectVersion projectVersion = ProjectBuilder
            .withProject(projectName)
            .withArtifact(Constants.ARTIFACT_TYPE) // R0
            .getCurrentVersion()
            .getProjectVersion();
        verifyProjectCreated(projectVersion);

        // Step - Download current project as JSON flat files
        List<File> projectFiles = new SafaRequest(AppRoutes.FlatFiles.DOWNLOAD_FLAT_FILES)
            .withVersion(projectVersion)
            .withFileType(DataFileBuilder.AcceptedFileTypes.JSON)
            .getWithFilesInZip();

        dbEntityBuilder.newProject("new project");
        ProjectVersion version = dbEntityBuilder.newVersionWithReturn("new project");

        // Step - Create files with flat files downloaded
        String newVersionIdString = SafaRequest
                .withRoute(AppRoutes.FlatFiles.UPDATE_PROJECT_VERSION_FROM_FLAT_FILES)
                .withVersion(version)
                .getFlatFileHelper()
                .postWithFiles(projectFiles, new JSONObject())
                .getJSONObject("projectVersion")
                .getString("versionId");

        // Step - Retrieve new project
        UUID newVersionId = UUID.fromString(newVersionIdString);
        ProjectVersion newProjectVersion = this.projectVersionRepository.findByVersionId(newVersionId);
        verifyProjectCreated(newProjectVersion);
    }

    private void verifyProjectCreated(ProjectVersion projectVersion) {
        // Step - Retrieve project
        ProjectAppEntity projectAppEntity = retrievalService.getProjectAtVersion(projectVersion);

        // VP - Verify that artifacts are created
        assertThat(projectAppEntity.getArtifacts()).hasSize(Constants.N_ARTIFACTS);

        // Step - Extract artifact information
        Map<String, ArtifactAppEntity> name2artifact = new HashMap<>();
        projectAppEntity
            .getArtifacts()
            .forEach(artifact -> name2artifact.put(artifact.getName(), artifact));

        // VP - Verify regular artifact
        String artifactName = Constants.ARTIFACT_NAMES.get(DocumentType.ARTIFACT_TREE);
        ArtifactAppEntity artifact = name2artifact.get(artifactName);
        assertThat(artifact.getType()).isEqualTo(Constants.ARTIFACT_TYPE);
        assertThat(artifact.getDocumentType()).isEqualTo(DocumentType.ARTIFACT_TREE);
    }

    protected static class Constants {
        static final int N_ARTIFACTS = 1;
        static final String ARTIFACT_TYPE = "requirements";
        static final Map<DocumentType, String> ARTIFACT_NAMES = Map.of(
            DocumentType.ARTIFACT_TREE, "R0"
        );
    }
}
