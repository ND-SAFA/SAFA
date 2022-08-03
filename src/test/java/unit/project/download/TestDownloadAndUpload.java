package unit.project.download;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.builders.entities.ProjectBuilder;
import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.flatfiles.services.DataFileBuilder;
import edu.nd.crc.safa.server.entities.app.project.FTAType;
import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.app.project.SafetyCaseType;
import edu.nd.crc.safa.server.entities.db.DocumentType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

/**
 * Creates a project containing one of each type of artifact and attempts to download and
 * re-upload the project.
 */
class TestDownloadAndUpload extends ApplicationBaseTest {
    String projectName = "project-name";
    String artifactType = "requirement";


    @Test
    void downloadAndCreateProject() throws Exception {
        setAuthorization();
        // Step - Create project with artifacts from docs: artifact tree, safety case, fta
        ProjectVersion projectVersion = createProject(projectName);
        verifyProjectCreated(projectVersion);

        // Step - Download current project as JSON flat files
        List<File> projectFiles = new SafaRequest(AppRoutes.Projects.FlatFiles.downloadFlatFiles)
            .withVersion(projectVersion)
            .withFileType(DataFileBuilder.AcceptedFileTypes.JSON)
            .getWithFilesInZip();

        // Step - Create files with flat files downloaded
        JSONObject newProjectJson = SafaRequest
            .withRoute(AppRoutes.Projects.FlatFiles.createProjectFromFlatFiles)
            .getFlatFileHelper()
            .postWithFiles(projectFiles);

        // Step - Retrieve new project
        String newVersionIdString = newProjectJson.getJSONObject("projectVersion").getString("versionId");
        UUID newVersionId = UUID.fromString(newVersionIdString);
        ProjectVersion newProjectVersion = this.projectVersionRepository.findByVersionId(newVersionId);
        verifyProjectCreated(newProjectVersion);
    }

    private void verifyProjectCreated(ProjectVersion projectVersion) {
        Project project = projectVersion.getProject();
        ProjectAppEntity projectAppEntity = getProjectAtVersion(projectVersion);
        // VP - Verify that artifacts are created
        assertThat(projectAppEntity.artifacts.size()).isEqualTo(Constants.N_ARTIFACTS);

        // Step - Extract artifact information
        List<DocumentType> documentTypes = new ArrayList<>();
        List<String> artifactNames = new ArrayList<>();
        List<SafetyCaseType> safetyCaseTypes = new ArrayList<>();
        List<FTAType> ftaTypes = new ArrayList<>();
        projectAppEntity
            .artifacts
            .forEach(artifact -> {
                documentTypes.add(artifact.getDocumentType());
                artifactNames.add(artifact.getName());
                safetyCaseTypes.add(artifact.getSafetyCaseType());
                ftaTypes.add(artifact.getLogicType());
            });

        // VP - Verify: artifact names, document types, safety case types, logic types
        assertListContains(artifactNames, Constants.ARTIFACT_NAMES);
        assertListContains(documentTypes, Constants.DOCUMENT_TYPES);
        assertListContains(safetyCaseTypes, Constants.SAFETY_CASE_TYPES);
        assertListContains(ftaTypes, Constants.FTA_TYPES);
    }

    private ProjectVersion createProject(String projectName) {
        // Step - Create regular artifact
        ProjectBuilder projectBuilder = ProjectBuilder
            .withProject(projectName)
            .withArtifact(artifactType) // R1
            .withSafetyArtifact(Constants.SAFETY_CASE_TYPE) // C1
            .withFtaArtifact(Constants.FTA_TYPE); // A1

        return projectBuilder.getCurrentVersion().getProjectVersion();
    }

    private <I> void assertListContains(List<I> items, I[] expected) {
        Arrays
            .stream(expected)
            .forEach(expectedItem -> assertThat(items.contains(expectedItem)).isTrue());
    }

    protected static class Constants {
        static final int N_SAFETY_ARTIFACTS = 1;
        static final int N_FTA_ARTIFACTS = 1;
        static final int N_ARTIFACTS = 3;

        static final SafetyCaseType SAFETY_CASE_TYPE = SafetyCaseType.CONTEXT;
        static final SafetyCaseType[] SAFETY_CASE_TYPES = new SafetyCaseType[]{SAFETY_CASE_TYPE};
        static final FTAType FTA_TYPE = FTAType.AND;
        static final DocumentType[] DOCUMENT_TYPES = new DocumentType[]{
            DocumentType.ARTIFACT_TREE,
            DocumentType.SAFETY_CASE,
            DocumentType.FTA
        };
        static final String[] ARTIFACT_NAMES = new String[]{
            "R0",
            "C0",
            "A0"
        };
        static final FTAType[] FTA_TYPES = new FTAType[]{
            FTA_TYPE,
        };
    }
}
