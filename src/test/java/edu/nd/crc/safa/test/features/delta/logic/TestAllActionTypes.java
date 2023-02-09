package edu.nd.crc.safa.test.features.delta.logic;

import static org.assertj.core.api.Assertions.assertThat;

import edu.nd.crc.safa.features.delta.entities.app.ProjectDelta;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.delta.services.DeltaService;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Responsible for testing incurring and validating each type of change is detected
 * and returned the delta calculation.
 */
class TestAllActionTypes extends ApplicationBaseTest {

    @Autowired
    DeltaService deltaService;

    @Test
    void testAllChangeTypes() {
        String projectName = "test-project";
        String artifactType = "requirement";
        String artifactName = "RE-8";
        String artifactSummary = "this is a summary";
        String artifactBody = "this is a body";
        String newArtifactBody = "this is a different body";

        // Step - Create project with: type, artifact, and body
        dbEntityBuilder
            .newProject(projectName)
            .newType(projectName, artifactType)
            .newVersion(projectName)
            .newArtifact(projectName, artifactType, artifactName)
            .newArtifactBody(projectName, artifactName, artifactSummary, artifactBody); // first body

        // VP - Delta against same version is empty
        ProjectVersion firstVersion = dbEntityBuilder.getProjectVersion(projectName, 0);
        ProjectDelta deltaZero = deltaService.calculateProjectDelta(firstVersion, firstVersion);

        assertThat(deltaZero.getArtifacts().getModified()).isEmpty();
        assertThat(deltaZero.getArtifacts().getRemoved()).isEmpty();
        assertThat(deltaZero.getArtifacts().getAdded()).isEmpty();

        // Step - Create second version with modified artifacts
        ProjectVersion secondVersion = dbEntityBuilder.newVersionWithReturn(projectName);
        dbEntityBuilder
            .newArtifactBody(projectName, 1, ModificationType.MODIFIED, artifactName, artifactSummary, newArtifactBody);

        // VP - Verify that system able to detect if modified
        ProjectDelta deltaOne = deltaService.calculateProjectDelta(firstVersion, secondVersion);
        assertThat(deltaOne.getArtifacts().getModified()).hasSize(1);
        assertThat(deltaOne.getArtifacts().getRemoved()).isEmpty();
        assertThat(deltaOne.getArtifacts().getAdded()).isEmpty();

        // VP - Remove artifact
        ProjectVersion thirdVersion = dbEntityBuilder.newVersionWithReturn(projectName);
        dbEntityBuilder
            .newArtifactBody(projectName, 2, ModificationType.REMOVED, artifactName, "", "");
        ProjectDelta deltaTwo = deltaService.calculateProjectDelta(secondVersion, thirdVersion);
        assertThat(deltaTwo.getArtifacts().getModified()).isEmpty();
        assertThat(deltaTwo.getArtifacts().getRemoved()).hasSize(1);
        assertThat(deltaTwo.getArtifacts().getAdded()).isEmpty();

        // VP - Remove artifact
        ProjectVersion fourthVersion = dbEntityBuilder.newVersionWithReturn(projectName);
        dbEntityBuilder
            .newArtifactBody(projectName, 3, artifactName, artifactSummary, artifactBody);
        ProjectDelta deltaThree = deltaService.calculateProjectDelta(thirdVersion, fourthVersion);
        assertThat(deltaThree.getArtifacts().getModified()).isEmpty();
        assertThat(deltaThree.getArtifacts().getRemoved()).isEmpty();
        assertThat(deltaThree.getArtifacts().getAdded()).hasSize(1);
    }
}
