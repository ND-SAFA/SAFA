package features.flatfiles.errors;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.config.ProjectPaths;

import features.jobs.base.AbstractUpdateProjectViaFlatFileTest;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Test that project with missing artifact file propagates error.
 */
class TestMissingArtifactFile extends AbstractUpdateProjectViaFlatFileTest {

    @Test
    void createProjectWithMissingArtifactFile() throws Exception {
        String missingArtifactFile = "Requirement.csv";
        JSONObject response = updateProjectViaFlatFiles(ProjectPaths.Tests.MISSING_DATA_FILE,
            status().is4xxClientError());
        String errorMessage = response.getString("message");
        assertThat(errorMessage).contains("missing").contains(missingArtifactFile);
    }
}
