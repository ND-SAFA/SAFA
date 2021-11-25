package unit.version;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.server.entities.api.ServerError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.services.VersionService;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.ApplicationBaseTest;

/**
 * Tests that system able to calculate and create the next version in a project.
 */
public class TestCreateNextRevision extends ApplicationBaseTest {
    @Autowired
    VersionService versionService;

    @Test
    public void createNextVersion() throws ServerError {
        String projectName = "test-project";
        dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName);

        Project project = dbEntityBuilder.getProject(projectName);
        ProjectVersion nextVersion = versionService.createNextRevision(project);
        assertThat(nextVersion.getMajorVersion()).isEqualTo(1);
        assertThat(nextVersion.getMinorVersion()).isEqualTo(1);
        assertThat(nextVersion.getRevision()).isEqualTo(2);
    }
}
