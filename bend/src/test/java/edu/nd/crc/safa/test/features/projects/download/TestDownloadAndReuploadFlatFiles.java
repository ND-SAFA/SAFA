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
import edu.nd.crc.safa.features.flatfiles.services.DataFileBuilder;
import edu.nd.crc.safa.features.jobs.entities.app.JobStatus;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;
import edu.nd.crc.safa.test.services.builders.ProjectBuilder;

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
        AuthorizationSetter.setSessionAuthorization(currentUserName, this.serviceProvider);
        // Step - Create project with artifacts from docs: artifact tree, safety case, fta
        ProjectVersion projectVersion = ProjectBuilder
            .withProject(projectName)
            .withArtifact(Constants.ARTIFACT_1_NAME, Constants.ARTIFACT_TYPE)
            .withArtifact(Constants.ARTIFACT_2_NAME, Constants.ARTIFACT_TYPE)
            .getCurrentVersion()
            .getProjectVersion();
        verifyProjectCreated(projectVersion);

        dbEntityBuilder
            .newTraceLink(projectName, Constants.ARTIFACT_1_NAME, Constants.ARTIFACT_2_NAME, 0);

        // Step - Download current project as JSON flat files
        List<File> projectFiles = new SafaRequest(AppRoutes.FlatFiles.DOWNLOAD_FLAT_FILES)
            .withVersion(projectVersion)
            .withFileType(DataFileBuilder.AcceptedFileTypes.JSON)
            .getWithFilesInZip();

        SafaRequest.withRoute(AppRoutes.Projects.DELETE_PROJECT_BY_ID)
            .withProject(projectVersion.getProject())
            .deleteWithJsonObject();

        JSONObject otherArgs = new JSONObject();
        otherArgs.put("name", "Project 2");
        otherArgs.put("description", "desc");

        // Step - Create files with flat files downloaded
        JSONObject response = SafaRequest
            .withRoute(AppRoutes.Jobs.Projects.PROJECT_BULK_UPLOAD)
            .getFlatFileHelper()
            .postWithFiles(projectFiles, otherArgs);

        assertThat(response.getString("status")).isEqualTo(JobStatus.COMPLETED.name());
        String projectId = response.getString("projectId");

        // Step - Retrieve new project
        Project project = serviceProvider.getProjectService().getProjectById(UUID.fromString(projectId));
        List<ProjectVersion> newProjectVersions = this.projectVersionRepository.findByProject(project);
        assertThat(newProjectVersions.size()).isEqualTo(1);
        ProjectAppEntity projectAppEntity = verifyProjectCreated(newProjectVersions.get(0));

        assertThat(projectAppEntity.getTraces().size()).isEqualTo(1);
        TraceAppEntity trace = projectAppEntity.getTraces().get(0);
        assertThat(projectAppEntity.getArtifacts().stream().anyMatch(a -> trace.getSourceId().equals(a.getId()))).isTrue();
        assertThat(projectAppEntity.getArtifacts().stream().anyMatch(a -> trace.getTargetId().equals(a.getId()))).isTrue();
    }

    private ProjectAppEntity verifyProjectCreated(ProjectVersion projectVersion) {
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
        ArtifactAppEntity artifact1 = name2artifact.get(Constants.ARTIFACT_1_NAME);
        assertThat(artifact1.getType()).isEqualTo(Constants.ARTIFACT_TYPE);
        ArtifactAppEntity artifact2 = name2artifact.get(Constants.ARTIFACT_2_NAME);
        assertThat(artifact2.getType()).isEqualTo(Constants.ARTIFACT_TYPE);

        return projectAppEntity;
    }

    protected static class Constants {
        static final int N_ARTIFACTS = 2;
        static final String ARTIFACT_TYPE = "requirements";

        static final String ARTIFACT_1_NAME = "artifact1";
        static final String ARTIFACT_2_NAME = "artifact2";
        static final String ARTIFACT_1_BODY = "body1";
        static final String ARTIFACT_2_BODY = "body2";
    }
}
