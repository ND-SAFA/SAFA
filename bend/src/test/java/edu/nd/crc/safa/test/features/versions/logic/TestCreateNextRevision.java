package edu.nd.crc.safa.test.features.versions.logic;

import static org.assertj.core.api.Assertions.assertThat;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.features.versions.services.VersionService;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Tests that system able to calculate and create the next version in a project.
 */
class TestCreateNextRevision extends ApplicationBaseTest {
    @Autowired
    VersionService versionService;

    @Test
    void createNextVersion() throws SafaError {
        dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName);

        Project project = dbEntityBuilder.getProject(projectName);
        ProjectVersion nextVersion = versionService.createNextRevision(project);

        // VP - Version has incremented
        assertThat(nextVersion.getMajorVersion()).isEqualTo(1);
        assertThat(nextVersion.getMinorVersion()).isZero();
        assertThat(nextVersion.getRevision()).isEqualTo(1);
    }
}
