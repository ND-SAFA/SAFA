package unit.db;

import static org.assertj.core.api.Assertions.assertThat;

import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

public class TestProjectVersion extends ApplicationBaseTest {

    @Test
    public void checkVersionIdIncremented() {
        // Step - Create project with two versions
        String projectName = "test-project";
        dbEntityBuilder.newProject(projectName);
        ProjectVersion sourceVersion1 = dbEntityBuilder.newVersionWithReturn(projectName);
        ProjectVersion sourceVersion2 = dbEntityBuilder.newVersionWithReturn(projectName);

        // VP - Verify that versions are incremented
        assertThat(sourceVersion1.isLessThanOrEqualTo(sourceVersion2)).isTrue();

        // Step - Create another project
        String otherProjectName = "other-project";
        dbEntityBuilder.newProject(otherProjectName);
        ProjectVersion targetVersion1 = dbEntityBuilder.newVersionWithReturn(otherProjectName);
        ProjectVersion targetVersion2 = dbEntityBuilder.newVersionWithReturn(otherProjectName);

        // VP - Verify that versions are incremented in other project
        assertThat(targetVersion1.isLessThanOrEqualTo(targetVersion2)).isTrue();
    }
}
