package unit.project.documents;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.List;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.db.Document;
import edu.nd.crc.safa.server.entities.db.DocumentType;
import edu.nd.crc.safa.server.entities.db.Project;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

/**
 * Tests that the client is create a new document for a project.
 */
public class CreateNewDocument extends ApplicationBaseTest {

    /**
     * Verifies that a new document can be created for a project.
     */
    @Test
    public void testCreateNewDocument() throws Exception {
        String projectName = "test-project";
        String docName = "test-document";
        String docDescription = "this is a description";
        DocumentType docType = DocumentType.ARTIFACT_TREE;

        // Step - Create empty project
        Project project = dbEntityBuilder.newProjectWithReturn(projectName);

        // Step - Create new document payload
        JSONObject docJson = jsonBuilder.createDocument(docName, docDescription, docType);

        // Step - Send creation request.
        String route = RouteBuilder.withRoute(AppRoutes.Projects.createOrUpdateDocument).withProject(project).get();
        JSONObject response = sendPost(route, docJson, status().isCreated());
        JSONObject docCreated = response.getJSONObject("body");

        // VP - Verify that response object contains name, description, and type
        assertThat(docCreated.getString("name")).isEqualTo(docName);
        assertThat(docCreated.getString("type")).isEqualTo(docType.toString());
        assertThat(docCreated.getString("description")).isEqualTo(docDescription);

        // VP - Verify single document created for project
        List<Document> projectDocuments = this.documentRepository.findByProject(project);
        assertThat(projectDocuments.size()).isEqualTo(1);

        // VP - Verify that persistent entity contains name, description, and type
        Document document = projectDocuments.get(0);
        assertThat(document.getName()).isEqualTo(docName);
        assertThat(document.getType()).isEqualTo(docType);
        assertThat(document.getDescription()).isEqualTo(docDescription);
    }
}
