package edu.nd.crc.safa.test.features.artifacts.properties;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.delta.entities.app.EntityDelta;
import edu.nd.crc.safa.features.delta.entities.app.ModifiedEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.services.builders.CommitBuilder;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.TextNode;
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
            .withArtifact(projectName, null, artifactName, type, body)
            .getArtifact(projectName, artifactName);

        // Step - Add custom fields
        JSONObject customFields = new JSONObject();
        customFields.put(fieldName, fieldValue);
        artifactJson.put("attributes", customFields);

        // Step - Save added artifact
        ProjectCommitDefinition commit = commitService.commit(CommitBuilder
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
        Map<String, JsonNode> customFieldsResponse = appEntity.getAttributes();
        assertEquals(customFieldsResponse.get(fieldName), TextNode.valueOf(fieldValue));

        // Step - Create second version
        ProjectVersion afterVersion = this.dbEntityBuilder.newVersionWithReturn(projectName);

        // Step - Add new field to `customFields`
        artifact.getAttributes().put(fieldName, TextNode.valueOf(newFieldValue));
        commitService.commit(CommitBuilder.withVersion(afterVersion).withModifiedArtifact(artifact));

        // Step - Get delta
        EntityDelta<ArtifactAppEntity> delta = this.artifactVersionRepository.calculateEntityDelta(projectVersion,
            afterVersion);
        Map<UUID, ModifiedEntity<ArtifactAppEntity>> modifiedArtifacts = delta.getModified();

        // VP - Verify change detected
        assertThat(modifiedArtifacts).containsKey(artifactId);
        ModifiedEntity<ArtifactAppEntity> modifiedArtifactEntity = modifiedArtifacts.get(artifactId);
        Object beforeValue = modifiedArtifactEntity.getBefore().getAttributes().get(fieldName);
        Object afterValue = modifiedArtifactEntity.getAfter().getAttributes().get(fieldName);
        assertThat(beforeValue).isEqualTo(TextNode.valueOf(fieldValue));
        assertThat(afterValue).isEqualTo(TextNode.valueOf(newFieldValue));
    }
}
