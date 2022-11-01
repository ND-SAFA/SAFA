package features.traces.logic;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
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
        createProjectWithTwoVersionsFromFlatFiles();
        ProjectVersion v1 = dbEntityBuilder.getProjectVersion(projectName, 0);
        ProjectVersion v2 = dbEntityBuilder.getProjectVersion(projectName, 1);
        Project project = v1.getProject();
        TraceLinkVersion link = traceLinkVersionRepository.getProjectLinks(project).get(0);

        // Step - Update in v1
        double testScore = 3.14;
        link.setScore(testScore);
        commitUpdateToTraceLink(link, v1);

        // VP - verify updates in V1
        Optional<TraceLinkVersion> linkDboV1 =
                traceLinkVersionRepository.findByProjectVersionAndTraceLink(v1, link.getTraceLink());
        assertThat(linkDboV1).isPresent();
        assertThat(linkDboV1.get().getScore()).isEqualTo(testScore);

        // VP - verify no update in V2
        Optional<TraceLinkVersion> linkDboV2 =
                traceLinkVersionRepository.findByProjectVersionAndTraceLink(v2, link.getTraceLink());
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
        createProjectWithTwoVersionsFromFlatFiles();
        ProjectVersion v1 = dbEntityBuilder.getProjectVersion(projectName, 0);
        ProjectVersion v2 = dbEntityBuilder.getProjectVersion(projectName, 1);
        Project project = v1.getProject();
        TraceLinkVersion link = traceLinkVersionRepository.getProjectLinks(project).get(0);

        // Step - Update in v2
        double testScore = 3.14;
        double currentScore = link.getScore();
        link.setScore(testScore);
        commitUpdateToTraceLink(link, v2);

        // VP - verify no updates in V1
        Optional<TraceLinkVersion> linkDboV1 =
                traceLinkVersionRepository.findByProjectVersionAndTraceLink(v1, link.getTraceLink());
        assertThat(linkDboV1).isPresent();
        assertThat(linkDboV1.get().getScore()).isEqualTo(currentScore);

        // VP - verify update in V2
        Optional<TraceLinkVersion> linkDboV2 =
                traceLinkVersionRepository.findByProjectVersionAndTraceLink(v2, link.getTraceLink());
        assertThat(linkDboV2).isPresent();
        assertThat(linkDboV2.get().getScore()).isEqualTo(testScore);
    }

    /**
     * Tests that deleting a trace link from V1 of a project actually deletes it instead of making
     * a new record showing a deletion.
     *
     * @throws Exception When loading from flat files fails
     */
    @Test
    void testDeleteFromV1() throws Exception {

        // Step - Create project with two versions
        createProjectWithTwoVersionsFromFlatFiles();
        ProjectVersion v1 = dbEntityBuilder.getProjectVersion(projectName, 0);
        ProjectVersion v2 = dbEntityBuilder.getProjectVersion(projectName, 1);
        Project project = v1.getProject();
        TraceLinkVersion link = traceLinkVersionRepository.getProjectLinks(project).get(0);

        // Step - Delete in v1
        commitDeletionOfTraceLink(link, v1);

        // VP - verify updates in V1
        Optional<TraceLinkVersion> linkDboV1 =
                traceLinkVersionRepository.findByProjectVersionAndTraceLink(v1, link.getTraceLink());
        assertThat(linkDboV1).isPresent();
        assertThat(linkDboV1.get().getModificationType()).isEqualTo(ModificationType.REMOVED);

        // VP - verify no update in V2
        Optional<TraceLinkVersion> linkDboV2 =
                traceLinkVersionRepository.findByProjectVersionAndTraceLink(v2, link.getTraceLink());
        assertThat(linkDboV2).isNotPresent();
    }

    /**
     * Tests that deleting a trace link from V2 of a project does not affect V1 and marks it as removed in V2.
     *
     * @throws Exception When loading from flat files fails
     */
    @Test
    void testDeleteFromV2() throws Exception {

        // Step - Create project with two versions
        createProjectWithTwoVersionsFromFlatFiles();
        ProjectVersion v1 = dbEntityBuilder.getProjectVersion(projectName, 0);
        ProjectVersion v2 = dbEntityBuilder.getProjectVersion(projectName, 1);
        Project project = v1.getProject();
        TraceLinkVersion link = traceLinkVersionRepository.getProjectLinks(project).get(0);

        // Step - Delete in v1
        commitDeletionOfTraceLink(link, v2);

        // VP - verify updates in V1
        Optional<TraceLinkVersion> linkDboV1 =
                traceLinkVersionRepository.findByProjectVersionAndTraceLink(v1, link.getTraceLink());
        assertThat(linkDboV1).isPresent();
        assertThat(linkDboV1.get().getModificationType()).isEqualTo(ModificationType.ADDED);

        // VP - verify no update in V2
        Optional<TraceLinkVersion> linkDboV2 =
                traceLinkVersionRepository.findByProjectVersionAndTraceLink(v2, link.getTraceLink());
        assertThat(linkDboV2).isPresent();
        assertThat(linkDboV2.get().getModificationType()).isEqualTo(ModificationType.REMOVED);
    }

    /**
     * Creates a new project with two versions both loaded from the MINI flat file. After the data is
     * loaded this method will assert that the project has a link and that the link has a version
     * in V1 but not in V2 (as it is not modified in that version).
     *
     * @throws Exception When loading from flat files fails
     */
    private void createProjectWithTwoVersionsFromFlatFiles() throws Exception {
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
    }

    /**
     * Utility method to commit changes to trace links.
     *
     * @param link Trace link with modifications
     * @param version Project version to create change in
     * @throws Exception If the commit fails
     */
    private void commitUpdateToTraceLink(TraceLinkVersion link, ProjectVersion version) throws Exception {
        TraceAppEntity linkAppEntity = this.traceLinkVersionRepository
                .retrieveAppEntityFromVersionEntity(link);
        commitService.commit(CommitBuilder
                .withVersion(version)
                .withModifiedTrace(linkAppEntity));
    }

    /**
     * Utility method to commit a deletion of a trace link.
     *
     * @param link Trace link to delete
     * @param version Project version to create change in
     * @throws Exception If the commit fails
     */
    private void commitDeletionOfTraceLink(TraceLinkVersion link, ProjectVersion version) throws Exception {
        TraceAppEntity linkAppEntity = this.traceLinkVersionRepository
                .retrieveAppEntityFromVersionEntity(link);
        commitService.commit(CommitBuilder
                .withVersion(version)
                .withRemovedTrace(linkAppEntity));
    }
}
