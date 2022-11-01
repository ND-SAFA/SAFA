package features.traces.logic;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import builders.CommitBuilder;
import common.ApplicationBaseTest;
import org.junit.jupiter.api.Test;
import requests.FlatFileRequest;

/**
 * Tests that versioning changes are detected for trace links.
 * <p>
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
        String flatFilesPath = ProjectPaths.Resources.Tests.MINI;
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

    /**
     * Tests that updates to a trace link in V1 of a project simply update the object
     * rather than creating a new version.
     *
     * @throws Exception When loading from flat files fails
     */
    @Test
    void testUpdateToV1() throws Exception {

        // Step - Create project with two versions
        dbEntityBuilder
                .newProject(projectName)
                .newVersion(projectName)
                .newVersion(projectName);
        ProjectVersion v1 = dbEntityBuilder.getProjectVersion(projectName, 0);
        ProjectVersion v2 = dbEntityBuilder.getProjectVersion(projectName, 1);
        Project project = v1.getProject();

        // Step - Import trace links into project versions
        String flatFilesPath = ProjectPaths.Resources.Tests.MINI;
        FlatFileRequest.updateProjectVersionFromFlatFiles(v1, flatFilesPath);
        FlatFileRequest.updateProjectVersionFromFlatFiles(v2, flatFilesPath);

        // VP - Verify trace link only exists in V1
        assertThat(traceLinkVersionRepository.getProjectLinks(project)).hasSize(1);
        TraceLinkVersion link = traceLinkVersionRepository.getProjectLinks(project).get(0);
        Optional<TraceLinkVersion> linkDboV1 =
                traceLinkVersionRepository.findByProjectVersionAndTraceLink(v1, link.getTraceLink());
        Optional<TraceLinkVersion> linkDboV2 =
                traceLinkVersionRepository.findByProjectVersionAndTraceLink(v2, link.getTraceLink());
        assertThat(linkDboV1).isPresent();
        assertThat(linkDboV2).isNotPresent();

        // Step - Update in v1
        double testScore = 3.14;
        link.setScore(testScore);
        TraceAppEntity linkAppEntity = this.traceLinkVersionRepository
                .retrieveAppEntityFromVersionEntity(link);
        commitService.commit(CommitBuilder
                .withVersion(v1)
                .withModifiedTrace(linkAppEntity));

        // VP - verify updates in V1
        linkDboV1 = traceLinkVersionRepository.findByProjectVersionAndTraceLink(v1, link.getTraceLink());
        assertThat(linkDboV1).isPresent();
        assertThat(linkDboV1.get().getScore()).isEqualTo(testScore);

        // VP - verify no update in V2
        linkDboV2 = traceLinkVersionRepository.findByProjectVersionAndTraceLink(v2, link.getTraceLink());
        assertThat(linkDboV2).isNotPresent();
    }

    /**
     * Tests that updates to a trace link in V2 of a project creates a new trace link version.
     *
     * @throws Exception When loading from flat files fails
     */
    @Test
    void testUpdateToV2() throws Exception {

        // Step - Create project with two versions
        dbEntityBuilder
                .newProject(projectName)
                .newVersion(projectName)
                .newVersion(projectName);
        ProjectVersion v1 = dbEntityBuilder.getProjectVersion(projectName, 0);
        ProjectVersion v2 = dbEntityBuilder.getProjectVersion(projectName, 1);
        Project project = v1.getProject();

        // Step - Import trace links into project versions
        String flatFilesPath = ProjectPaths.Resources.Tests.MINI;
        FlatFileRequest.updateProjectVersionFromFlatFiles(v1, flatFilesPath);
        FlatFileRequest.updateProjectVersionFromFlatFiles(v2, flatFilesPath);

        // VP - Verify trace link only exists in V1
        assertThat(traceLinkVersionRepository.getProjectLinks(project)).hasSize(1);
        TraceLinkVersion link = traceLinkVersionRepository.getProjectLinks(project).get(0);
        Optional<TraceLinkVersion> linkDboV1 =
                traceLinkVersionRepository.findByProjectVersionAndTraceLink(v1, link.getTraceLink());
        Optional<TraceLinkVersion> linkDboV2 =
                traceLinkVersionRepository.findByProjectVersionAndTraceLink(v2, link.getTraceLink());
        assertThat(linkDboV1).isPresent();
        assertThat(linkDboV2).isNotPresent();

        // Step - Update in v2
        double testScore = 3.14;
        double currentScore = link.getScore();
        link.setScore(testScore);
        TraceAppEntity linkAppEntity = this.traceLinkVersionRepository
                .retrieveAppEntityFromVersionEntity(link);
        commitService.commit(CommitBuilder
                .withVersion(v2)
                .withModifiedTrace(linkAppEntity));

        // VP - verify no updates in V1
        linkDboV1 = traceLinkVersionRepository.findByProjectVersionAndTraceLink(v1, link.getTraceLink());
        assertThat(linkDboV1).isPresent();
        assertThat(linkDboV1.get().getScore()).isEqualTo(currentScore);

        // VP - verify update in V2
        linkDboV2 = traceLinkVersionRepository.findByProjectVersionAndTraceLink(v2, link.getTraceLink());
        assertThat(linkDboV2).isPresent();
        assertThat(linkDboV2.get().getScore()).isEqualTo(testScore);
    }
}
