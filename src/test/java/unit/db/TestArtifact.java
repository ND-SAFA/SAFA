package unit.db;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.Optional;

import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactType;

import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

/**
 * Verifies that an artifact is able to be created, retrieved, updated,
 * and deleted.
 */
public class TestArtifact extends ApplicationBaseTest {

    @Test
    public void createRetrieveUpdateDeleteArtifact() {
        String projectName = "test_project";
        String artifactTypeName = "design definitions";
        String artifactName = "RE-8";
        String newArtifactName = "RE-10";

        // Step - Create project with artifact
        this.dbEntityBuilder.newProject(projectName);
        ArtifactType artifactType = dbEntityBuilder.newTypeAndReturn(projectName, artifactTypeName);
        Artifact artifact = dbEntityBuilder.newArtifactWithReturn(projectName, artifactTypeName, artifactName);

        //VP 2 - Retrieve artifact
        Optional<Artifact> queriedArtifact = this.artifactRepository.findById(artifact.getArtifactId());

        assertThat(queriedArtifact.isPresent()).isTrue();
        Artifact artifactFound = queriedArtifact.get();
        assertThat(artifactFound.getBaseEntityId()).isEqualTo(artifactName);
        assertThat(artifactFound.getType().getTypeId()).isEqualTo(artifactType.getTypeId());

        // VP - Update artifact name and confirm update
        dbEntityBuilder.updateArtifactName(projectName, artifactName, newArtifactName);

        queriedArtifact = this.artifactRepository.findById(artifact.getArtifactId());
        assertThat(queriedArtifact.isPresent()).isTrue();
        artifactFound = queriedArtifact.get();
        assertThat(artifactFound.getBaseEntityId()).isEqualTo(newArtifactName);
        assertThat(artifactFound.getType().getTypeId()).isEqualTo(artifactType.getTypeId());

        // VP - Update artifact name and confirm update
        this.artifactRepository.deleteById(artifact.getArtifactId());
        queriedArtifact = this.artifactRepository.findById(artifact.getArtifactId());
        assertThat(queriedArtifact.isPresent()).isFalse();
    }
}
