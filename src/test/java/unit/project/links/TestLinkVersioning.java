package unit.project.links;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.api.ProjectEntities;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

/**
 * Tests that versioning changes are detected for trace links.
 * <p>
 * TODO: Test that modification is detected
 * TODO: Test that removal is detected
 */
public class TestLinkVersioning extends ApplicationBaseTest {

    String projectName = "project-name";

    /**
     * Tests that an identical trace submitted to the next version is not stored
     * as an entry.
     *
     * @throws Exception If http requests fails
     */
    @Test
    public void testNoChangeDetected() throws Exception {

        // Step - Create project with two versions: base and target
        dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newVersion(projectName);
        ProjectVersion v1 = dbEntityBuilder.getProjectVersion(projectName, 0);
        ProjectVersion v2 = dbEntityBuilder.getProjectVersion(projectName, 1);
        Project project = v1.getProject();

        // Step - Create base trace link
        String flatFilesPath = ProjectPaths.PATH_TO_MINI_FILES;
        uploadFlatFilesToVersion(v1, flatFilesPath);

        // VP - Verify that link is stored as added
        ProjectEntities baseEntities = appEntityRetrievalService.retrieveProjectEntitiesAtProjectVersion(v1);
        List<TraceAppEntity> baseTraces = baseEntities.getProject().getTraces();
        assertThat(baseTraces.size()).isEqualTo(1);

        // Step - Save same link to latter version
        uploadFlatFilesToVersion(v2, flatFilesPath);

        // VP - Verify that no change is stored by system
        assertThat(this.traceLinkVersionRepository.getProjectLinks(project).size()).isEqualTo(1);

        // VP - Verify that retrieving link from target version.
        ProjectEntities targetEntities = appEntityRetrievalService.retrieveProjectEntitiesAtProjectVersion(v1);
        List<TraceAppEntity> targetTraces = targetEntities.getProject().getTraces();
        assertThat(targetTraces.size()).isEqualTo(1);
    }
}
