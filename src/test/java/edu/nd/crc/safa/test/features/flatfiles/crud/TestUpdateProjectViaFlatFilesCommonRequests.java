package edu.nd.crc.safa.test.features.flatfiles.crud;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.common.DefaultProjectConstants;
import edu.nd.crc.safa.test.requests.FlatFileRequest;

import org.junit.jupiter.api.Test;

class TestUpdateProjectViaFlatFilesCommonRequests extends ApplicationBaseTest {

    @Test
    void testUpdateProjectViaFlatFiles() throws Exception {
        String projectName = "test-project";

        dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newVersion(projectName)
            .newVersion(projectName);

        Project project = dbEntityBuilder.getProject(projectName);
        ProjectVersion emptyVersion = dbEntityBuilder.getProjectVersion(projectName, 0);
        ProjectVersion updateVersion = dbEntityBuilder.getProjectVersion(projectName, 1);
        ProjectVersion noChangeVersion = dbEntityBuilder.getProjectVersion(projectName, 2);

        // Step - Create request to update project via flat files
        FlatFileRequest.updateProjectVersionFromFlatFiles(updateVersion,
            ProjectPaths.Resources.Tests.DefaultProject.V1);

        // VP - Verify that no artifacts associated with empty version
        List<ArtifactVersion> initialBodies = this.artifactVersionRepository.findByProjectVersion(emptyVersion);
        assertThat(initialBodies)
            .as("no bodies at init")
            .isEmpty();

        // VP - Verify that artifacts are constructed and associated with update version
        List<ArtifactVersion> updateBodies = this.artifactVersionRepository.findByProjectVersion(updateVersion);
        assertThat(updateBodies)
            .as("bodies created in later version")
            .hasSize(DefaultProjectConstants.Entities.N_ARTIFACTS);
        List<TraceLinkVersion> updateTraces = this.traceLinkVersionRepository.getApprovedLinksInProject(project);
        assertThat(updateTraces).hasSize(DefaultProjectConstants.Entities.N_LINKS);

        // Step - Create request to parse same flat files at different version
        FlatFileRequest.updateProjectVersionFromFlatFiles(noChangeVersion,
            ProjectPaths.Resources.Tests.DefaultProject.V1);

        // VP - No new artifacts were created
        List<ArtifactVersion> noChangeBodies = this.artifactVersionRepository.findByProjectVersion(noChangeVersion);
        assertThat(noChangeBodies)
            .as("no changes were detected in project versions")
            .isEmpty();

        // VP - No new trace links were created
        List<TraceLinkVersion> noChangeTraces = this.traceLinkVersionRepository.getApprovedLinksInProject(project);
        assertThat(noChangeTraces).hasSize(DefaultProjectConstants.Entities.N_LINKS);
    }
}
