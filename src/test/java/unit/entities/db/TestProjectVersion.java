package unit.entities.db;

import static org.assertj.core.api.Assertions.assertThat;

import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;

import org.junit.jupiter.api.Test;
import unit.EntityBaseTest;

public class TestProjectVersion extends EntityBaseTest {

    @Test
    public void checkVersionIdIncremented() {
        // Step - Create project with two versions
        String projectName = "test-project";
        entityBuilder.newProject(projectName);
        ProjectVersion sourceVersion1 = entityBuilder.newVersionWithReturn(projectName);
        ProjectVersion sourceVersion2 = entityBuilder.newVersionWithReturn(projectName);

        // VP - Verify that versions are incremented
        assertThat(sourceVersion1.isLessThanOrEqualTo(sourceVersion2)).isTrue();

        // Step - Create another project
        String otherProjectName = "other-project";
        entityBuilder.newProject(otherProjectName);
        ProjectVersion targetVersion1 = entityBuilder.newVersionWithReturn(otherProjectName);
        ProjectVersion targetVersion2 = entityBuilder.newVersionWithReturn(otherProjectName);

        // VP - Verify that versions are incremented in other project
        assertThat(targetVersion1.isLessThanOrEqualTo(targetVersion2)).isTrue();
    }
}
