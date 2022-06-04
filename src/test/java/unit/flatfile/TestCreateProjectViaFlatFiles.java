package unit.flatfile;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.db.Project;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.request.MockMultipartHttpServletRequestBuilder;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

public class TestCreateProjectViaFlatFiles extends FlatFileBaseTest {

    @Test
    public void testUseCase() throws Exception {

        // Step 1 - Upload flat files
        String routeName = AppRoutes.Projects.FlatFiles.projectFlatFiles;
        MockMultipartHttpServletRequestBuilder request = createMultiPartRequest(routeName,
            ProjectPaths.PATH_TO_DEFAULT_PROJECT);
        JSONObject responseBody = sendRequest(request, MockMvcResultMatchers.status().isCreated(), this.token);

        // VP - Verify response contains entities
        Project project = verifyBeforeResponse(responseBody);

        // VP - Verify that entities were actually created
        verifyDefaultProjectEntities(project);
    }
}
