package unit.project.documents;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.documents.entities.app.DocumentColumnDataType;
import edu.nd.crc.safa.features.documents.entities.db.DocumentColumn;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;
import edu.nd.crc.safa.features.documents.repositories.DocumentColumnRepository;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Tests that the client is create a new document for a project.
 */
class TestCreateFmeaDocument extends DocumentBaseTest {

    @Autowired
    DocumentColumnRepository documentColumnRepository;

    /**
     * Verifies that a new document can be created for a project.
     */
    @Test
    void testCreateFmeaDocument() throws Exception {
        DocumentType docType = DocumentType.FMEA;
        String columnName = "Artifact ID";
        String newColumnName = "NEW COLUMN NAME";
        DocumentColumnDataType newColumnType = DocumentColumnDataType.FREE_TEXT;
        DocumentColumnDataType columnType = DocumentColumnDataType.SELECT;

        // Step - Create empty project
        ProjectVersion projectVersion = dbEntityBuilder.newProject(projectName).newVersionWithReturn(projectName);

        // Step - Create new document payload
        JSONObject requestedDocumentJson = jsonBuilder.createFMEADocument(docName, docDescription);
        List<JSONObject> columns = List.of(jsonBuilder.createDocumentColumn(null, columnName, columnType));
        requestedDocumentJson.put("columns", columns);

        // Step - Send creation request.
        JSONObject responseDocumentJson = createOrUpdateDocumentJson(projectVersion, requestedDocumentJson);

        // VP - Assert document base entity properties were returned
        String documentId = responseDocumentJson.getString("documentId");
        assertObjectsMatch(requestedDocumentJson, responseDocumentJson, List.of("id", "columns"));
        assertThat(documentId).isNotEmpty();

        // VP - Assert columns properties were returned in response
        JSONObject documentColumnJson = assertDocumentColumns(responseDocumentJson, 1).getJSONObject(0);
        assertDocumentColumnJson(documentColumnJson, columnName, columnType);

        // VP - Verify that document base entity is persisted.
        assertDocumentInProjectExists(projectVersion.getProject(), docName, docDescription, docType);

        // VP - Verify that columns were persisted
        List<DocumentColumn> documentColumns = documentColumnRepository
            .findByDocumentDocumentIdOrderByTableColumnIndexAsc(UUID.fromString(documentId));
        assertThat(documentColumns.size()).isEqualTo(1);
        DocumentColumn documentColumn = documentColumns.get(0);
        assertDocumentColumn(documentColumn, columnName, columnType, 0);

        // Step - Create new column in front of previous
        List<JSONObject> newColumns = List.of(jsonBuilder.createDocumentColumn(null, newColumnName, newColumnType),
            documentColumnJson);
        responseDocumentJson.put("columns", newColumns);

        //Step - Update columns
        JSONObject updateResponseJson = createOrUpdateDocumentJson(projectVersion, responseDocumentJson);

        // VP - Assert columns properties were returned in response
        JSONArray updatedColumnsJson = updateResponseJson.getJSONArray("columns");
        JSONObject newColumnJson = assertDocumentColumns(updateResponseJson, 2).getJSONObject(0);
        assertDocumentColumnJson(newColumnJson, newColumnName, newColumnType);

        // VP - Verify that columns were persisted
        List<DocumentColumn> updatedDocumentColumns = documentColumnRepository
            .findByDocumentDocumentIdOrderByTableColumnIndexAsc(UUID.fromString(documentId));
        assertThat(updatedDocumentColumns.size()).isEqualTo(2);
        DocumentColumn updatedDocumentColumn = updatedDocumentColumns.get(0);
        assertDocumentColumn(updatedDocumentColumn, newColumnName, newColumnType, 0);

        // Step - Retrieve document
        JSONArray documentsRetrieved = getProjectDocuments(projectVersion.getProject());

        // VP - Verify single document retrieved
        assertThat(documentsRetrieved.length()).isEqualTo(1);
        JSONObject documentJson = documentsRetrieved.getJSONObject(0);
        assertThat(documentJson.get("type")).isEqualTo(docType.toString());

        // VP - Verify that columns match too
        JSONObject expectedColumns = new JSONObject();
        JSONObject actualColumns = new JSONObject();

        expectedColumns.put("columns", updatedColumnsJson);
        actualColumns.put("columns", documentJson.getJSONArray("columns"));

        assertObjectsMatch(expectedColumns, actualColumns);
    }

    private JSONArray assertDocumentColumns(JSONObject object,
                                            int expectedLength
    ) {
        JSONArray documentColumnsJson = object.getJSONArray("columns");
        assertThat(documentColumnsJson.length()).isEqualTo(expectedLength);
        return documentColumnsJson;
    }

    private void assertDocumentColumnJson(JSONObject documentColumnJson, String name, DocumentColumnDataType columnType) {
        assertThat(documentColumnJson.getString("id")).isNotEmpty();
        assertThat(documentColumnJson.getString("name")).isEqualTo(name);
        assertThat(documentColumnJson.getString("dataType")).isEqualTo(columnType.toString());
    }

    private void assertDocumentColumn(DocumentColumn documentColumn,
                                      String name,
                                      DocumentColumnDataType dataType,
                                      int tableColumnIndex) {
        assertThat(documentColumn.getName()).isEqualTo(name);
        assertThat(documentColumn.getDataType()).isEqualTo(dataType);
        assertThat(documentColumn.getTableColumnIndex()).isEqualTo(tableColumnIndex);
    }
}
