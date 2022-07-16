package unit.project.artifacts;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.lang.reflect.Field;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.builders.CommitBuilder;
import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.db.DocumentType;
import edu.nd.crc.safa.server.entities.db.IArtifact;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.artifacts.IProjectEntityRetriever;

import org.javatuples.Pair;
import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

/**
 * Responsible for providing utilities functions for testing:
 * 1. Creation of artifacts
 * 2. Modification of artifacts
 * 3. Delta of artifacts
 * 4. Deletion of artifacts
 * 5. Recreation of artifacts
 */
public abstract class ArtifactBaseTest<T extends IArtifact> extends ApplicationBaseTest {
    String projectName = "test-project";
    String projectDescription = "project-description";
    String artifactName = "RE-10";
    String artifactBody = "this is a body";
    String newArtifactBody = "this is a new body";
    String documentName = "document-name";
    String documentDescription = "document-description";
    String documentId;

    public abstract JSONObject getArtifactJson(String projectName, String artifactName, String artifactBody);

    public abstract String getArtifactType();

    public abstract DocumentType getDocumentType();

    public abstract Map<String, Object> getJsonExpectedProperties();

    public abstract IProjectEntityRetriever<T> getArtifactRepository();

    public abstract Class getArtifactClass();

    public Map<String, Object> getEntityExpectedProperties() {
        return getJsonExpectedProperties();
    }

    @Test
    public void test() throws Exception {
        // Step - Create project with artifact type
        ProjectVersion projectVersion = dbEntityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);

        // VP - Verify that artifact is created
        Pair<JSONObject, T> artifactCreated = testCreation(projectVersion);

        // VP - Verify that modification is detected by delta.
        // TODO: Test delta of artifact type specific properties (e.g. customProperties)
        testArtifactDelta(projectVersion, artifactCreated.getValue0());

        // VP - Verify that artifact is deleted
        testDeletion(projectVersion, artifactCreated.getValue0());

        // VP - Verify that artifact can be re-created
        testCreation(projectVersion);
    }

    /**
     * Tests that when an artifact is created that:
     * 1. Correct information is returned in commit response.
     * 2. Correct information is persisted in the database.
     *
     * @return The JSON of the created artifact and the artifact itself.
     * @throws Exception Throws exception is error occurs while committing artifact.
     */
    protected Pair<JSONObject, T> testCreation(ProjectVersion projectVersion) throws Exception {
        // Step - Create artifact type
        if (!this.dbEntityBuilder.hasType(projectName, this.getArtifactType())) {
            dbEntityBuilder.newType(projectName, this.getArtifactType());
        }

        // Step - Create document if not exists
        if (documentId == null) {
            documentId = createDocument(projectVersion);
        }

        // Step - Create artifact json
        JSONObject artifactJson = this.getArtifactJson(projectName, artifactName, artifactBody);
        artifactJson.put("documentIds", List.of(documentId));

        // Step - Send artifact creation request
        CommitBuilder commitBuilder = CommitBuilder
            .withVersion(projectVersion)
            .withAddedArtifact(artifactJson);
        JSONObject commitResponseJson = commit(commitBuilder);

        // VP - Verify single artifact returned in response
        JSONArray artifactsAddedJson = commitResponseJson.getJSONObject("artifacts").getJSONArray("added");
        assertThat(artifactsAddedJson.length()).isEqualTo(1);

        // VP - Verify artifact name, id, and document type is correct
        JSONObject artifactAddedJson = artifactsAddedJson.getJSONObject(0);
        assertThat(artifactAddedJson.getString("name")).isEqualTo(artifactName);
        assertThat(artifactAddedJson.getString("id")).isNotEmpty();
        assertThat(artifactAddedJson.getString("documentType")).isEqualTo(this.getDocumentType().toString());

        for (Map.Entry<String, Object> entry : this.getJsonExpectedProperties().entrySet()) {
            assertThat(artifactAddedJson.get(entry.getKey()).toString()).isEqualTo(entry.getValue().toString());
        }

        // VP - Verify that single artifact was persisted in project
        List<T> projectArtifacts = this.getArtifactRepository().getByProject(projectVersion.getProject());
        assertThat(projectArtifacts.size()).isEqualTo(1);

        // VP - Verify persisted information is correct
        T projectArtifact = projectArtifacts.get(0);
        assertThat(projectArtifact.getName()).isEqualTo(artifactName);
        for (Map.Entry<String, Object> entry : this.getEntityExpectedProperties().entrySet()) {
            Object value = this.getField(projectArtifact, entry.getKey());
            assertThat(value).isEqualTo(entry.getValue());
        }

        return new Pair<>(artifactAddedJson, projectArtifact);
    }

    /**
     * Tests that artifact is deleted and no artifacts exists in system after.
     *
     * @param projectVersion - The project version to commit the deletion to.
     * @param artifactJson   - The artifact json whose being deleted.
     * @throws Exception Throws exception is commit fails.
     */
    protected void testDeletion(ProjectVersion projectVersion, JSONObject artifactJson) throws Exception {
        // Step - Delete artifact
        CommitBuilder deleteCommitBuilder =
            CommitBuilder.withVersion(projectVersion).withRemovedArtifact(artifactJson);
        commit(deleteCommitBuilder);

        // VP - Verify that artifact no longer exists in database
        List<T> projectArtifacts = this.getArtifactRepository().getByProject(projectVersion.getProject());
        assertThat(projectArtifacts.size()).isEqualTo(1);
    }

    protected void testArtifactDelta(ProjectVersion baselineVersion, JSONObject artifactJson) throws Exception {
        ProjectVersion newProjectVersion = this.dbEntityBuilder.newVersionWithReturn(projectName);
        String artifactId = artifactJson.getString("id");
        artifactJson.put("body", newArtifactBody);

        // Step - Commit modified artifact
        commit(CommitBuilder
            .withVersion(newProjectVersion)
            .withModifiedArtifact(artifactJson));

        // Step - Get project delta
        String deltaRouteName = RouteBuilder
            .withRoute(AppRoutes.Projects.Delta.calculateProjectDelta)
            .withBaselineVersion(baselineVersion)
            .withTargetVersion(newProjectVersion)
            .buildEndpoint();
        JSONObject projectDelta = sendGet(deltaRouteName);

        // VP - Verify that change is detected
        JSONObject modifiedArtifacts = projectDelta.getJSONObject("artifacts").getJSONObject("modified");
        JSONObject modifiedArtifact = modifiedArtifacts.getJSONObject(artifactId);
        assertThat(modifiedArtifact.getJSONObject("before").getString("body")).isEqualTo(artifactBody);
        assertThat(modifiedArtifact.getJSONObject("after").getString("body")).isEqualTo(newArtifactBody);
    }

    public Object getField(T o, String strKey) throws NoSuchFieldException, IllegalAccessException {
        Class tmp = this.getArtifactClass();
        Field field = tmp.getDeclaredField(strKey);
        field.setAccessible(true);
        return field.get(o);
    }

    private String createDocument(ProjectVersion projectVersion) throws Exception {
        // Step - Create new document payload
        JSONObject requestedDocumentJson = this.createDocumentJson();

        // Step - Send creation request.
        JSONObject documentJson = createOrUpdateDocumentJson(projectVersion, requestedDocumentJson);
        return documentJson.getString("documentId");
    }

    protected JSONObject createDocumentJson() {
        DocumentType documentType = this.getDocumentType();
        switch (documentType) {
            case SAFETY_CASE:
                return jsonBuilder.createFMEADocument(documentName, documentDescription);
            default:
                return jsonBuilder.createDocument(documentName, documentDescription, documentType);
        }
    }
}
