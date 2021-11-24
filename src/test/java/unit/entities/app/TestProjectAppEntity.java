package unit.entities.app;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;

import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.db.Artifact;

import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

/**
 * Validates and verifies accuracy of methods adding functionality to ApplicationModel class.
 */
public class TestProjectAppEntity extends ApplicationBaseTest {

    @Test
    public void ableToDetectNewArtifacts() {
        String projectName = "test-project";
        String artifactTypeName = "Requirement";
        String newArtifactName = "RE-8";
        String existingArtifactName = "RE-10";

        // Step - Create project containing single artifact
        dbEntityBuilder
            .newProject(projectName)
            .newType(projectName, artifactTypeName)
            .newArtifact(projectName, artifactTypeName, existingArtifactName);

        // Step - Create update payload with new artifact (RE-8)
        appBuilder
            .withProject(projectName)
            .withArtifact(projectName, newArtifactName)
            .withArtifact(projectName, existingArtifactName);

        // VP - ProjectAppEntity is able to detect the new artifacts
        List<Artifact> existingArtifacts = dbEntityBuilder.getArtifacts(projectName);
        ProjectAppEntity appEntity = appBuilder.getProject(projectName);
        List<ArtifactAppEntity> newArtifacts = appEntity.findNewArtifacts(existingArtifacts);

        assertThat(newArtifacts.size()).as("# new artifacts").isEqualTo(1);
        assertThat(newArtifacts.get(0).getName()).as("new artifact names").isEqualTo(newArtifactName);
    }
}
