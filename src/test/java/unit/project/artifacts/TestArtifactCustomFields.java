package unit.project.artifacts;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.Hashtable;
import java.util.Map;

import edu.nd.crc.safa.builders.CommitBuilder;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.EntityDelta;
import edu.nd.crc.safa.server.entities.app.ModifiedEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.artifacts.ArtifactVersionRepository;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.ApplicationBaseTest;

public class TestArtifactCustomFields extends ApplicationBaseTest {

    @Autowired
    ArtifactVersionRepository artifactVersionRepository;

    /**
     * Tests that the user is able to create a new artifact containing
     * custom fields.
     */
    @Test
    public void createWithFields() throws Exception {
        String projectName = "test";
        String artifactName = "RE-20";
        String type = "requirements";
        String body = "this is body";
        String fieldName = "field-name";
        String fieldValue = "field-value";
        String newFieldValue = "new-" + fieldValue;

        ProjectVersion projectVersion = this.dbEntityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);

        // Step - Create artifact json
        JSONObject artifactJson = this.jsonBuilder
            .withProject(projectName, projectName, "")
            .withArtifact(projectName, "", artifactName, type, body)
            .getArtifact(projectName, artifactName);

        // Step - Add custom fields
        JSONObject customFields = new JSONObject();
        customFields.put(fieldName, fieldValue);
        artifactJson.put("customFields", customFields);

        // Step - Save added artifact
        JSONObject response = commit(CommitBuilder
            .withVersion(projectVersion)
            .withAddedArtifact(artifactJson));

        // VP - Verify that artifact was added
        JSONArray artifactsAddedJson = response.getJSONObject("artifacts").getJSONArray("added");
        assertThat(artifactsAddedJson.length()).isEqualTo(1);
        String artifactId = artifactsAddedJson.getJSONObject(0).getString("id");

        // VP - Verify that custom fields persisted
        ArtifactAppEntity appEntity =
            artifactVersionRepository.retrieveAppEntitiesByProjectVersion(projectVersion).get(0);
        Map<String, String> customFieldsResponse = appEntity.customFields;
        assertThat(customFieldsResponse.size()).isEqualTo(1);
        assertThat(customFieldsResponse.containsKey(fieldName)).isTrue();
        assertThat(customFieldsResponse.get(fieldName)).isEqualTo(fieldValue);

        // Step - Create second version
        ProjectVersion afterVersion = this.dbEntityBuilder.newVersionWithReturn(projectName);

        // Step - Update fields
        JSONObject artifactJsonResponse = artifactsAddedJson.getJSONObject(0);
        artifactJsonResponse.getJSONObject("customFields").put(fieldName, newFieldValue);

        // Step - Commit changes to new version
        commit(CommitBuilder.withVersion(afterVersion).withModifiedArtifact(artifactJsonResponse));

        // Step - Get delta
        EntityDelta<ArtifactAppEntity> delta = this.artifactVersionRepository.calculateEntityDelta(projectVersion,
            afterVersion);
        Hashtable<String, ModifiedEntity<ArtifactAppEntity>> modifiedArtifacts = delta.getModified();

        // VP - Verify change detected
        assertThat(modifiedArtifacts.containsKey(artifactId)).isTrue();
        ModifiedEntity<ArtifactAppEntity> modifiedArtifactEntity = modifiedArtifacts.get(artifactId);
        String beforeValue = modifiedArtifactEntity.getBefore().getCustomFields().get(fieldName);
        String afterValue = modifiedArtifactEntity.getAfter().getCustomFields().get(fieldName);
        assertThat(beforeValue).isEqualTo(fieldValue);
        assertThat(afterValue).isEqualTo(newFieldValue);
    }
}
