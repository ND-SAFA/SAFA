package edu.nd.crc.safa.test.features.flatfiles.logic;

import static org.assertj.core.api.Assertions.assertThat;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.flatfiles.controllers.entities.ArtifactNameCheck;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;
import edu.nd.crc.safa.test.services.builders.CommitBuilder;
import edu.nd.crc.safa.test.services.builders.ProjectBuilder;
import edu.nd.crc.safa.utilities.JsonFileUtilities;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;

class TestCheckArtifactName extends ApplicationBaseTest {

    @Test
    void testNameAvailable() throws Exception {
        String artifactName = "RE-20";
        ProjectVersion projectVersion = this.dbEntityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);

        assertThat(doesArtifactExists(projectVersion, artifactName)).isFalse();
    }

    /**
     * Test that if artifact created in V1 but deleted in V2:
     * - is unavailable in V1
     * - is available in V2
     */
    @Test
    public void testAvailableIfDeleted() throws Exception {
        // Step - Create project, v1, artifact, and v2
        String artifactType = "requirements";
        String artifactName = "R0";
        ProjectBuilder
            .withProject(projectName) // Creates V1 automatically
            .withArtifact(artifactType)
            .withVersion();
        ProjectVersion v1 = this.dbEntityBuilder.getProjectVersion(projectName, 0);
        ProjectVersion v2 = this.dbEntityBuilder.getProjectVersion(projectName, 1);

        // VP - Verify unavailable in all versions
        assertThat(doesArtifactExists(v1, artifactName)).isTrue();
        assertThat(doesArtifactExists(v2, artifactName)).isTrue();

        // Step - Delete artifact
        JSONObject artifactJson = getArtifactJson(artifactName, 0);
        CommitBuilder deleteCommit = CommitBuilder
            .withVersion(v2)
            .withRemovedArtifact(artifactJson);
        commitService.commit(deleteCommit);

        // VP - Verify that
        assertThat(doesArtifactExists(v1, artifactName)).isTrue();
        assertThat(doesArtifactExists(v2, artifactName)).isFalse();
    }

    private boolean doesArtifactExists(ProjectVersion projectVersion, String artifactName) throws Exception {
        return SafaRequest
            .withRoute(AppRoutes.Projects.Entities.CHECK_IF_ARTIFACT_EXISTS)
            .withVersion(projectVersion)
            .postWithJsonObject(new ArtifactNameCheck(artifactName))
            .getBoolean(ProjectVariables.ARTIFACT_EXISTS);
    }

    private JSONObject getArtifactJson(String artifactName, int versionIndex) {
        ArtifactVersion artifactVersion = this.dbEntityBuilder.getArtifactBody(projectName, artifactName, versionIndex);
        ArtifactAppEntity artifactAppEntity = new ArtifactAppEntity();
        artifactAppEntity.setId(artifactVersion.getArtifact().getArtifactId());
        artifactAppEntity.setName(artifactVersion.getName());
        return JsonFileUtilities.toJson(artifactAppEntity);
    }
}
