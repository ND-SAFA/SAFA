package unit.flatfile;

import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.db.Project;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;

class TestCreateProjectViaFlatFiles extends FlatFileBaseTest {

    @Test
    void testUseCase() throws Exception {

        // Step 1 - Upload flat files
        JSONObject responseBody = SafaRequest
            .withRoute(AppRoutes.Projects.FlatFiles.createProjectFromFlatFiles)
            .getFlatFileHelper()
            .uploadFlatFilesToVersion(ProjectPaths.PATH_TO_DEFAULT_PROJECT);

        // VP - Verify response contains entities
        Project project = verifyDefaultProjectCreationResponse(responseBody);

        // VP - Verify that entities were actually created
        verifyDefaultProjectEntities(project);
    }
}
