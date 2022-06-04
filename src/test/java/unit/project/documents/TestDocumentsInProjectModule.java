package unit.project.documents;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.common.AppRoutes;
import edu.nd.crc.safa.server.entities.db.DocumentType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

/**
 * Tests that a user is able to delete a document in a project.
 */
public class TestDocumentsInProjectModule extends ApplicationBaseTest {

    /**
     * Verifies that a root document is
     */
    @Test
    public void testRootDocumentCreatedWithProject() throws Exception {
        String projectName = "test-project";

        // Step - Create empty project
        ProjectVersion projectVersion = dbEntityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);
        Project project = projectVersion.getProject();

        // Step - Retrieve project
        String route = RouteBuilder
            .withRoute(AppRoutes.Projects.Entities.getProjectInVersion)
            .withVersion(projectVersion)
            .get();
        JSONObject projectJson = sendGet(route, status().isOk());

        // VP - Verify that documents has empty list
        assertThat(projectJson.getJSONArray("documents").length()).isEqualTo(0);

        // Step - Create a document
        String docName = "this is a random title";
        String docDescription = "this is a document description.";
        DocumentType docType = DocumentType.ARTIFACT_TREE;
        dbEntityBuilder.newDocument(projectName, docName, docDescription, docType);

        // VP - Verify that project meta data contains a single document
        projectJson = sendGet(route, status().isOk());
        JSONArray documentsJson = projectJson.getJSONArray("documents");
        assertThat(documentsJson.length()).isEqualTo(1);

        // VP - Verify that single documents contains correct name, description, and type
        JSONObject docJson = documentsJson.getJSONObject(0);
        assertThat(docJson.getString("name")).isEqualTo(docName);
        assertThat(docJson.getString("description")).isEqualTo(docDescription);
        assertThat(docJson.getString("type")).isEqualTo(docType.toString());
    }
}
