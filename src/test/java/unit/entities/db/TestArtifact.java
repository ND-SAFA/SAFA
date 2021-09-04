package unit.entities.db;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.Optional;

import edu.nd.crc.safa.db.entities.sql.Artifact;
import edu.nd.crc.safa.db.entities.sql.ArtifactType;

import org.junit.jupiter.api.Test;
import unit.EntityBaseTest;

/**
 * Verifies that an artifact is able to be created, retrieved, updated,
 * and deleted.
 */
public class TestArtifact extends EntityBaseTest {

    @Test
    public void createRetrieveUpdateDeleteArtifact() {
        String projectName = "test_project";
        String artifactTypeName = "design definitions";
        String artifactName = "RE-8";
        String newArtifactName = "RE-10";

        // Step - Create project with artifact
        this.entityBuilder.newProject(projectName);
        ArtifactType artifactType = entityBuilder.newTypeAndReturn(projectName, artifactTypeName);
        Artifact artifact = entityBuilder.newArtifactWithReturn(projectName, artifactTypeName, artifactName);

        //VP 2 - Retrieve artifact
        Optional<Artifact> queriedArtifact = this.artifactRepository.findById(artifact.getArtifactId());

        assertThat(queriedArtifact.isPresent()).isTrue();
        Artifact artifactFound = queriedArtifact.get();
        assertThat(artifactFound.getName()).isEqualTo(artifactName);
        assertThat(artifactFound.getType().getTypeId()).isEqualTo(artifactType.getTypeId());

        // VP - Update artifact name and confirm update
        entityBuilder.updateArtifactName(projectName, artifactName, newArtifactName);

        queriedArtifact = this.artifactRepository.findById(artifact.getArtifactId());
        assertThat(queriedArtifact.isPresent()).isTrue();
        artifactFound = queriedArtifact.get();
        assertThat(artifactFound.getName()).isEqualTo(newArtifactName);
        assertThat(artifactFound.getType().getTypeId()).isEqualTo(artifactType.getTypeId());

        // VP - Update artifact name and confirm update
        this.artifactRepository.deleteById(artifact.getArtifactId());
        queriedArtifact = this.artifactRepository.findById(artifact.getArtifactId());
        assertThat(queriedArtifact.isPresent()).isFalse();
    }
}
