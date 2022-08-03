package unit.project.documents;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

/**
 * Tests that a user is able to delete a document in a project.
 */
class TestDocumentsInProjectModule extends ApplicationBaseTest {

    /**
     * Verifies that a root document is
     */
    @Test
    void testRootDocumentCreatedWithProject() throws Exception {
        String projectName = "test-project";

        // Step - Create empty project
        ProjectVersion projectVersion = dbEntityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);
        Project project = projectVersion.getProject();

        // Step - Retrieve project
        JSONObject projectJson = SafaRequest
            .withRoute(AppRoutes.Projects.Entities.GET_PROJECT_IN_VERSION)
            .withVersion(projectVersion)
            .getWithJsonObject();

        // VP - Verify that documents has empty list
        assertThat(projectJson.getJSONArray("documents").length()).isZero();

        // Step - Create a document
        String docName = "this is a random title";
        String docDescription = "this is a document description.";
        DocumentType docType = DocumentType.ARTIFACT_TREE;
        dbEntityBuilder.newDocument(projectName, docName, docDescription, docType);

        // VP - Verify that project meta data contains a single document
        projectJson = SafaRequest
            .withRoute(AppRoutes.Projects.Entities.GET_PROJECT_IN_VERSION)
            .withVersion(projectVersion)
            .getWithJsonObject();
        JSONArray documentsJson = projectJson.getJSONArray("documents");
        assertThat(documentsJson.length()).isEqualTo(1);

        // VP - Verify that single documents contains correct name, description, and type
        JSONObject docJson = documentsJson.getJSONObject(0);
        assertThat(docJson.getString("name")).isEqualTo(docName);
        assertThat(docJson.getString("description")).isEqualTo(docDescription);
        assertThat(docJson.getString("type")).isEqualTo(docType.toString());
    }
}
