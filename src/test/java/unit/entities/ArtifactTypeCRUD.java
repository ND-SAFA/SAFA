package unit.entities;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.entities.database.ArtifactType;
import edu.nd.crc.safa.entities.database.Project;

import org.junit.jupiter.api.Test;
import unit.EntityBaseTest;

/* Tests that ArtifactTypes can be created
 *
 */
public class ArtifactTypeCRUD extends EntityBaseTest {
    @Test
    public void createRetrieveUpdateDeleteArtifactType() {
        String projectName = "test_project";
        String artifactTypeName = "Design Definitions";
        String altArtifactTypeName = "Requirements";

        Project project = createProject(projectName);

        //VP 1 - Create Artifact Type
        ArtifactType artifactType = new ArtifactType(project, artifactTypeName);
        artifactTypeRepository.save(artifactType);
        UUID artifactTypeId = artifactType.getTypeId();
        assertThat(artifactTypeId).isNotNull();

        //VP 2 - Retrieve Artifact Type
        ArtifactType queriedArtifactType = artifactTypeRepository.findByTypeId(artifactTypeId);

        assertThat(queriedArtifactType).isNotNull();
        assertThat(queriedArtifactType.getName()).isEqualTo(artifactTypeName.toLowerCase());

        //VP 3 - Update Artifact Type
        queriedArtifactType.setName(altArtifactTypeName);
        artifactTypeRepository.save(queriedArtifactType);
        queriedArtifactType = artifactTypeRepository.findByTypeId(artifactTypeId);
        assertThat(queriedArtifactType.getName()).isEqualTo(altArtifactTypeName.toLowerCase());

        //VP 4 - Delete Artifact Type
        artifactTypeRepository.delete(queriedArtifactType);
        Optional<ArtifactType> artifactTypeQuery = artifactTypeRepository.findById(artifactTypeId);

        assertThat(artifactTypeQuery.isPresent()).isFalse();
    }
}
