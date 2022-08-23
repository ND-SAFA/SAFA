package features.artifacts.properties;


import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.delta.entities.app.EntityDelta;
import edu.nd.crc.safa.features.delta.entities.app.ModifiedEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import builders.CommitBuilder;
import features.base.ApplicationBaseTest;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

class TestArtifactCustomFields extends ApplicationBaseTest {

    @Autowired
    ArtifactVersionRepository artifactVersionRepository;

    /**
     * Tests that the user is able to create a new artifact containing
     * custom fields.
     */
    @Test
    void createWithFields() throws Exception {
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
        ProjectCommit commit = commitService.commit(CommitBuilder
            .withVersion(projectVersion)
            .withAddedArtifact(artifactJson));

        // VP - Verify that artifact was added
        List<ArtifactAppEntity> artifactsAdded = commit.getArtifacts().getAdded();
        assertThat(artifactsAdded).hasSize(1);

        // Step - Extract artifact
        ArtifactAppEntity artifact = artifactsAdded.get(0);
        String artifactId = artifact.getId();

        // VP - Verify that custom fields persisted
        ArtifactAppEntity appEntity =
            artifactVersionRepository.retrieveAppEntitiesByProjectVersion(projectVersion).get(0);
        Map<String, String> customFieldsResponse = appEntity.getCustomFields();
        assertThat(customFieldsResponse)
            .hasSize(1)
            .containsEntry(fieldName, fieldValue);

        // Step - Create second version
        ProjectVersion afterVersion = this.dbEntityBuilder.newVersionWithReturn(projectName);

        // Step - Add new field to `customFields`
        artifact.getCustomFields().put(fieldName, newFieldValue);
        commitService.commit(CommitBuilder.withVersion(afterVersion).withModifiedArtifact(artifact));

        // Step - Get delta
        EntityDelta<ArtifactAppEntity> delta = this.artifactVersionRepository.calculateEntityDelta(projectVersion,
            afterVersion);
        Map<String, ModifiedEntity<ArtifactAppEntity>> modifiedArtifacts = delta.getModified();

        // VP - Verify change detected
        assertThat(modifiedArtifacts).containsKey(artifactId);
        ModifiedEntity<ArtifactAppEntity> modifiedArtifactEntity = modifiedArtifacts.get(artifactId);
        String beforeValue = modifiedArtifactEntity.getBefore().getCustomFields().get(fieldName);
        String afterValue = modifiedArtifactEntity.getAfter().getCustomFields().get(fieldName);
        assertThat(beforeValue).isEqualTo(fieldValue);
        assertThat(afterValue).isEqualTo(newFieldValue);
    }
}
