package features.jobs.logic.common;

import static org.junit.jupiter.api.Assertions.assertThrows;

import java.io.IOException;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.entities.jobs.CreateProjectViaJsonJob;
import edu.nd.crc.safa.features.tgen.entities.TraceGenerationRequest;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import common.ApplicationBaseTest;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Tests that the generic job worker is parsing step correctly.
 */
class TestJobMethodExtraction extends ApplicationBaseTest {

    @Autowired
    ServiceProvider serviceProvider;
    ProjectVersion projectVersion;

    @Test
    void testErrorThrownOnMethodNotFound() throws IOException {
        this.projectVersion = creationService.createDefaultProject("project");
        assertThrows(RuntimeException.class, () -> {
            buildProjectCreationJob().getMethodForStepByName("no exist");
        });
    }

    private CreateProjectViaJsonJob buildProjectCreationJob() {
        return new CreateProjectViaJsonJob(
            new JobDbEntity(),
            serviceProvider,
            new ProjectCommit(projectVersion, false),
            new TraceGenerationRequest()
        );
    }
}
