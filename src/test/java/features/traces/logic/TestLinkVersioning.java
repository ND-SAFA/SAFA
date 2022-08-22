package features.traces.logic;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;

import requests.FlatFileRequest;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import features.base.ApplicationBaseTest;
import org.junit.jupiter.api.Test;

/**
 * Tests that versioning changes are detected for trace links.
 * <p>
 * TODO: Test that modification is detected
 * TODO: Test that removal is detected
 */
class TestLinkVersioning extends ApplicationBaseTest {

    /**
     * Tests that an identical trace submitted to the next version is not stored
     * as an entry.
     *
     * @throws Exception If http requests fails
     */
    @Test
    void testNoChangeDetected() throws Exception {

        // Step - Create project with two versions: base and target
        dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newVersion(projectName);
        ProjectVersion v1 = dbEntityBuilder.getProjectVersion(projectName, 0);
        ProjectVersion v2 = dbEntityBuilder.getProjectVersion(projectName, 1);
        Project project = v1.getProject();

        // Step - Create base trace link
        String flatFilesPath = ProjectPaths.Tests.MINI;
        FlatFileRequest.updateProjectVersionFromFlatFiles(v1, flatFilesPath);

        // VP - Verify that link is stored as added
        ProjectAppEntity baseEntities = retrievalService.getProjectAtVersion(v1);
        List<TraceAppEntity> baseTraces = baseEntities.getTraces();
        assertThat(baseTraces).hasSize(1);

        // Step - Save same link to latter version
        FlatFileRequest.updateProjectVersionFromFlatFiles(v2, flatFilesPath);

        // VP - Verify that no change is stored by system
        assertThat(this.traceLinkVersionRepository.getProjectLinks(project)).hasSize(1);

        // VP - Verify that retrieving link from target version.
        ProjectAppEntity targetEntities = retrievalService.getProjectAtVersion(v1);
        List<TraceAppEntity> targetTraces = targetEntities.getTraces();
        assertThat(targetTraces).hasSize(1);
    }
}
