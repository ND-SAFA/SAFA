package features.projects.download;

import static org.assertj.core.api.Assertions.assertThat;

import java.io.File;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.builders.entities.ProjectBuilder;
import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.FTAType;
import edu.nd.crc.safa.features.artifacts.entities.SafetyCaseType;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.flatfiles.services.DataFileBuilder;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import common.AuthorizationTestService;
import features.base.ApplicationBaseTest;
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
        AuthorizationTestService.setAuthorization(this.serviceProvider);
        // Step - Create project with artifacts from docs: artifact tree, safety case, fta
        ProjectVersion projectVersion = ProjectBuilder
            .withProject(projectName)
            .withArtifact(Constants.ARTIFACT_TYPE) // R0
            .withSafetyArtifact(Constants.SAFETY_CASE_TYPE) // C0
            .withFtaArtifact(Constants.FTA_TYPE) // A0
            .getCurrentVersion()
            .getProjectVersion();
        verifyProjectCreated(projectVersion);

        // Step - Download current project as JSON flat files
        List<File> projectFiles = new SafaRequest(AppRoutes.FlatFiles.DOWNLOAD_FLAT_FILES)
            .withVersion(projectVersion)
            .withFileType(DataFileBuilder.AcceptedFileTypes.JSON)
            .getWithFilesInZip();

        // Step - Create files with flat files downloaded
        String newVersionIdString = SafaRequest
            .withRoute(AppRoutes.FlatFiles.CREATE_NEW_PROJECT_FROM_FLAT_FILES)
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
        ProjectAppEntity projectAppEntity = retrievalTestService.getProjectAtVersion(projectVersion);

        // VP - Verify that artifacts are created
        assertThat(projectAppEntity.artifacts).hasSize(Constants.N_ARTIFACTS);

        // Step - Extract artifact information
        Map<String, ArtifactAppEntity> name2artifact = new HashMap<>();
        projectAppEntity
            .artifacts
            .forEach(artifact -> name2artifact.put(artifact.name, artifact));

        // VP - Verify regular artifact
        String artifactName = Constants.ARTIFACT_NAMES.get(DocumentType.ARTIFACT_TREE);
        ArtifactAppEntity artifact = name2artifact.get(artifactName);
        assertThat(artifact.type).isEqualTo(Constants.ARTIFACT_TYPE);
        assertThat(artifact.getDocumentType()).isEqualTo(DocumentType.ARTIFACT_TREE);
        assertThat(artifact.getSafetyCaseType()).isNull();
        assertThat(artifact.getLogicType()).isNull();

        // VP - Verify safety artifact
        String safetyArtifactName = Constants.ARTIFACT_NAMES.get(DocumentType.SAFETY_CASE);
        ArtifactAppEntity safetyArtifact = name2artifact.get(safetyArtifactName);
        assertThat(safetyArtifact.type).isEqualTo(Constants.SAFETY_CASE_TYPE.name());
        assertThat(safetyArtifact.getDocumentType()).isEqualTo(DocumentType.SAFETY_CASE);
        assertThat(safetyArtifact.getSafetyCaseType()).isEqualTo(Constants.SAFETY_CASE_TYPE);
        assertThat(safetyArtifact.getLogicType()).isNull();

        // VP - Verify FTA artifact
        String logicArtifactName = Constants.ARTIFACT_NAMES.get(DocumentType.FTA);
        ArtifactAppEntity logicArtifact = name2artifact.get(logicArtifactName);
        assertThat(logicArtifact.type).isEqualTo(Constants.FTA_TYPE.name());
        assertThat(logicArtifact.getDocumentType()).isEqualTo(DocumentType.FTA);
        assertThat(logicArtifact.getSafetyCaseType()).isNull();
        assertThat(logicArtifact.getLogicType()).isEqualTo(Constants.FTA_TYPE);
    }

    protected static class Constants {
        static final int N_ARTIFACTS = 3;
        static final String ARTIFACT_TYPE = "requirements";
        static final SafetyCaseType SAFETY_CASE_TYPE = SafetyCaseType.CONTEXT;
        static final FTAType FTA_TYPE = FTAType.AND;
        static final Map<DocumentType, String> ARTIFACT_NAMES = new HashMap<DocumentType, String>() {{
            put(DocumentType.ARTIFACT_TREE, "R0");
            put(DocumentType.SAFETY_CASE, "C0");
            put(DocumentType.FTA, "A0");
        }};
    }
}
