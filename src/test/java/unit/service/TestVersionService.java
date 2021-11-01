package unit.service;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.api.ServerError;
import edu.nd.crc.safa.server.services.VersionService;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.EntityBaseTest;

public class TestVersionService extends EntityBaseTest {
    @Autowired
    VersionService versionService;

    @Test
    public void createNextVersion() throws ServerError {
        String projectName = "test-project";
        entityBuilder
            .newProject(projectName)
            .newVersion(projectName);

        Project project = entityBuilder.getProject(projectName);
        ProjectVersion nextVersion = versionService.createNextRevision(project);
        assertThat(nextVersion.getMajorVersion()).isEqualTo(1);
        assertThat(nextVersion.getMinorVersion()).isEqualTo(1);
        assertThat(nextVersion.getRevision()).isEqualTo(2);
    }
}
