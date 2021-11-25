package unit.entities.db;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.ArtifactType;

import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

/**
 * Tests that ArtifactTypes can be created, retrieved, updated, and deleted.
 */
public class TestArtifactType extends ApplicationBaseTest {
    @Test
    public void createRetrieveUpdateDeleteArtifactType() {
        String projectName = "test_project";
        String artifactTypeName = "Design Definitions";
        String altArtifactTypeName = "Requirements";

        // Step - Create project with new artifact type
        this.dbEntityBuilder.newProject(projectName);
        ArtifactType artifactType = dbEntityBuilder.newTypeAndReturn(projectName, artifactTypeName);

        // VP - Artifact type created
        UUID artifactTypeId = artifactType.getTypeId();
        ArtifactType queriedArtifactType = artifactTypeRepository.findByTypeId(artifactTypeId);

        assertThat(artifactTypeId).isNotNull();
        assertThat(queriedArtifactType).isNotNull();
        assertThat(queriedArtifactType.getName()).isEqualTo(artifactTypeName.toLowerCase());

        // VP 3 - Update type name
        dbEntityBuilder.updateTypeName(projectName, artifactTypeName, altArtifactTypeName);
        queriedArtifactType = artifactTypeRepository.findByTypeId(artifactTypeId);
        assertThat(queriedArtifactType.getName()).isEqualTo(altArtifactTypeName.toLowerCase());

        // VP - Delete Artifact Type
        artifactTypeRepository.delete(queriedArtifactType);
        Optional<ArtifactType> artifactTypeQuery = artifactTypeRepository.findById(artifactTypeId);
        assertThat(artifactTypeQuery.isPresent()).isFalse();
    }
}
