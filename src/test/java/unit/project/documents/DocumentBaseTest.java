package unit.project.documents;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.db.Document;
import edu.nd.crc.safa.server.entities.db.DocumentType;
import edu.nd.crc.safa.server.entities.db.Project;

import org.json.JSONArray;
import unit.ApplicationBaseTest;

/**
 * Tests that the client is create a new document for a project.
 */
public abstract class DocumentBaseTest extends ApplicationBaseTest {

    String projectName = "test-project";
    String docName = "test-document";
    String docDescription = "this is a description";


    protected void assertDocumentInProjectExists(Project project,
                                                 String docName,
                                                 String docDescription,
                                                 DocumentType docType) {
        assertDocumentInProjectExists(project,
            docName,
            docDescription,
            docType,
            new ArrayList<>());
    }

    protected void assertDocumentInProjectExists(Project project,
                                                 String docName,
                                                 String docDescription,
                                                 DocumentType docType,
                                                 List<String> artifactIds) {
        List<Document> projectDocuments = this.documentRepository.findByProject(project);
        assertThat(projectDocuments.size()).isEqualTo(1);

        // VP - Verify that persistent entity contains name, description, and type
        Document document = projectDocuments.get(0);
        assertThat(document.getName()).isEqualTo(docName);
        assertThat(document.getType()).isEqualTo(docType);
        assertThat(document.getDescription()).isEqualTo(docDescription);

        // VP - Verify that only the artifactIds given exist
        List<String> documentArtifactIds = this.documentArtifactRepository.findByDocument(document)
            .stream()
            .map(da -> da.getArtifact().getArtifactId().toString())
            .collect(Collectors.toList());
        assertThat(artifactIds.size()).isEqualTo(documentArtifactIds.size());
        assertTrue(artifactIds.containsAll(documentArtifactIds));
        assertTrue(documentArtifactIds.containsAll(artifactIds));
    }


    protected JSONArray getProjectDocuments(Project project) throws Exception {
        return SafaRequest
            .withRoute(AppRoutes.Projects.Documents.GET_PROJECT_DOCUMENTS)
            .withProject(project)
            .getWithJsonArray();
    }
}
