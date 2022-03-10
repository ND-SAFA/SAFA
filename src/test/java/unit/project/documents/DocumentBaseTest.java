package unit.project.documents;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Iterator;
import java.util.List;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.db.Document;
import edu.nd.crc.safa.server.entities.db.DocumentType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.json.JSONObject;
import unit.ApplicationBaseTest;

/**
 * Tests that the client is create a new document for a project.
 */
public class DocumentBaseTest extends ApplicationBaseTest {

    String projectName = "test-project";
    String docName = "test-document";
    String docDescription = "this is a description";


    protected void assertDocumentInProjectExists(Project project,
                                                 String docName,
                                                 String docDescription,
                                                 DocumentType docType) {
        List<Document> projectDocuments = this.documentRepository.findByProject(project);
        assertThat(projectDocuments.size()).isEqualTo(1);

        // VP - Verify that persistent entity contains name, description, and type
        Document document = projectDocuments.get(0);
        assertThat(document.getName()).isEqualTo(docName);
        assertThat(document.getType()).isEqualTo(docType);
        assertThat(document.getDescription()).isEqualTo(docDescription);
    }

    protected JSONObject createDocument(ProjectVersion projectVersion, JSONObject docJson) throws Exception {
        // Step - Send creation request.
        String route =
            RouteBuilder
                .withRoute(AppRoutes.Projects.createOrUpdateDocument)
                .withVersion(projectVersion)
                .get();
        return sendPost(route, docJson, status().isCreated());
    }

    protected void assertObjectsMatch(JSONObject docCreated, JSONObject docJson) {

        // VP - Verify that response object contains name, description, and type
        for (Iterator<String> it = docJson.keys(); it.hasNext(); ) {
            String key = it.next();
            assertThat(docCreated.get(key)).isEqualTo(docJson.get(key));
        }
    }
}
