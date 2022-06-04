package unit.flatfile;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;

import java.util.List;

import edu.nd.crc.safa.common.ProjectPaths;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceLinkVersion;

import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;
import unit.SampleProjectConstants;

public class TestUpdateProjectViaFlatFiles extends ApplicationBaseTest {

    @Test
    public void testUpdateProjectViaFlatFiles() throws Exception {
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
        uploadFlatFilesToVersion(updateVersion, ProjectPaths.PATH_TO_BEFORE_FILES);

        // VP - Verify that no artifacts associated with empty version
        List<ArtifactVersion> initialBodies = this.artifactVersionRepository.findByProjectVersion(emptyVersion);
        assertThat(initialBodies.size())
            .as("no bodies at init")
            .isEqualTo(0);

        // VP - Verify that artifacts are constructed and associated with update version
        List<ArtifactVersion> updateBodies = this.artifactVersionRepository.findByProjectVersion(updateVersion);
        assertThat(updateBodies.size())
            .as("bodies created in later version")
            .isEqualTo(SampleProjectConstants.N_ARTIFACTS);
        List<TraceLinkVersion> updateTraces = this.traceLinkVersionRepository.getApprovedLinksInProject(project);
        assertThat(updateTraces.size()).isEqualTo(SampleProjectConstants.N_LINKS);

        // Step - Create request to parse same flat files at different version
        uploadFlatFilesToVersion(noChangeVersion, ProjectPaths.PATH_TO_BEFORE_FILES);

        // VP - No new artifacts were created
        List<ArtifactVersion> noChangeBodies = this.artifactVersionRepository.findByProjectVersion(noChangeVersion);
        assertThat(noChangeBodies.size())
            .as("no changes were detected in project versions")
            .isEqualTo(0);

        // VP - No new trace links were created
        List<TraceLinkVersion> noChangeTraces = this.traceLinkVersionRepository.getApprovedLinksInProject(project);
        assertThat(noChangeTraces.size()).isEqualTo(SampleProjectConstants.N_LINKS);
    }
}
