package edu.nd.crc.safa.test.features.documents.base;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONArray;

/**
 * Tests that the client is create a new document for a project.
 */
public abstract class AbstractDocumentTest extends ApplicationBaseTest {

    protected String projectName = "test-project";
    protected String docName = "test-document";
    protected String docDescription = "this is a description";

    protected void assertDocumentInProjectExists(Project project,
                                                 String docName,
                                                 String docDescription) {
        assertDocumentInProjectExists(project,
            docName,
            docDescription,
            new ArrayList<>());
    }

    protected void assertDocumentInProjectExists(Project project,
                                                 String docName,
                                                 String docDescription,
                                                 List<String> artifactIds) {
        List<Document> projectDocuments = this.documentRepository.findByProject(project);
        assertThat(projectDocuments).hasSize(1);

        // VP - Verify that persistent entity contains name, description, and type
        Document document = projectDocuments.get(0);
        assertThat(document.getName()).isEqualTo(docName);
        assertThat(document.getDescription()).isEqualTo(docDescription);

        // VP - Verify that only the artifactIds given exist
        List<String> documentArtifactIds = this.documentArtifactRepository.findByDocument(document)
            .stream()
            .map(da -> da.getArtifact().getArtifactId().toString())
            .collect(Collectors.toList());
        assertThat(artifactIds).hasSize(documentArtifactIds.size());
        assertTrue(artifactIds.containsAll(documentArtifactIds));
        assertTrue(documentArtifactIds.containsAll(artifactIds));
    }

    protected JSONArray getProjectDocuments(ProjectVersion projectVersion) throws Exception {
        return SafaRequest
            .withRoute(AppRoutes.Documents.GET_PROJECT_DOCUMENTS)
            .withVersion(projectVersion)
            .getWithJsonArray();
    }
}
