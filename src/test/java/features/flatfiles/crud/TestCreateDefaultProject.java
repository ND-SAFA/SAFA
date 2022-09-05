package features.flatfiles.crud;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import features.flatfiles.base.BaseFlatFileTest;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import requests.SafaRequest;

/**
 * Creates default project via flat files and verifies:
 * - all entities were created
 * - parsing errors were returned
 */
class TestCreateDefaultProject extends BaseFlatFileTest {

    @Test
    void testUseCase() throws Exception {
        // Step 1 - Upload flat files
        JSONObject responseBody = SafaRequest
            .withRoute(AppRoutes.FlatFiles.CREATE_NEW_PROJECT_FROM_FLAT_FILES)
            .getFlatFileHelper()
            .postWithFilesInDirectory(ProjectPaths.Resources.Tests.DefaultProject.V1, new JSONObject());

        // VP - Verify response contains entities
        Project project = verifyDefaultProjectCreationResponse(responseBody);

        // VP - Verify that entities were actually created
        verifyDefaultProjectEntities(project);
    }
}
