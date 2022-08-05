package unit.flatfile;

import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;

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
            .withRoute(AppRoutes.Projects.FlatFiles.CREATE_PROJECT_FROM_FLAT_FILES)
            .getFlatFileHelper()
            .postWithFilesInDirectory(ProjectPaths.PATH_TO_DEFAULT_PROJECT);

        // VP - Verify response contains entities
        Project project = verifyDefaultProjectCreationResponse(responseBody);

        // VP - Verify that entities were actually created
        verifyDefaultProjectEntities(project);
    }
}
