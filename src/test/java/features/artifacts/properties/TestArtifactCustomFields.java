package features.artifacts.properties;


import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeType;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.delta.entities.app.EntityDelta;
import edu.nd.crc.safa.features.delta.entities.app.ModifiedEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import builders.CommitBuilder;
import common.ApplicationBaseTest;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;

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
            .newCustomAttribute(projectName, CustomAttributeType.TEXT, fieldName, fieldName)
            .newVersionWithReturn(projectName);

        // Step - Create artifact json
        JSONObject artifactJson = this.jsonBuilder
            .withProject(projectName, projectName, "")
            .withArtifact(projectName, null, artifactName, type, body)
            .getArtifact(projectName, artifactName);

        // Step - Add custom fields
        JSONObject customFields = new JSONObject();
        customFields.put(fieldName, fieldValue);
        artifactJson.put("attributes", customFields);

        // Step - Save added artifact
        ProjectCommit commit = commitService.commit(CommitBuilder
            .withVersion(projectVersion)
            .withAddedArtifact(artifactJson));

        // VP - Verify that artifact was added
        List<ArtifactAppEntity> artifactsAdded = commit.getArtifacts().getAdded();
        assertThat(artifactsAdded).hasSize(1);

        // Step - Extract artifact
        ArtifactAppEntity artifact = artifactsAdded.get(0);
        UUID artifactId = artifact.getId();

        // VP - Verify that custom fields persisted
        ArtifactAppEntity appEntity =
            artifactVersionRepository.retrieveAppEntitiesByProjectVersion(projectVersion).get(0);
        Map<String, String> customFieldsResponse = appEntity.getAttributes();
        assertThat(customFieldsResponse)
            .hasSize(1)
            .containsEntry(fieldName, fieldValue);

        // Step - Create second version
        ProjectVersion afterVersion = this.dbEntityBuilder.newVersionWithReturn(projectName);

        // Step - Add new field to `customFields`
        artifact.getAttributes().put(fieldName, newFieldValue);
        commitService.commit(CommitBuilder.withVersion(afterVersion).withModifiedArtifact(artifact));

        // Step - Get delta
        EntityDelta<ArtifactAppEntity> delta = this.artifactVersionRepository.calculateEntityDelta(projectVersion,
            afterVersion);
        Map<UUID, ModifiedEntity<ArtifactAppEntity>> modifiedArtifacts = delta.getModified();

        // VP - Verify change detected
        assertThat(modifiedArtifacts).containsKey(artifactId);
        ModifiedEntity<ArtifactAppEntity> modifiedArtifactEntity = modifiedArtifacts.get(artifactId);
        String beforeValue = modifiedArtifactEntity.getBefore().getAttributes().get(fieldName);
        String afterValue = modifiedArtifactEntity.getAfter().getAttributes().get(fieldName);
        assertThat(beforeValue).isEqualTo(fieldValue);
        assertThat(afterValue).isEqualTo(newFieldValue);
    }
}
