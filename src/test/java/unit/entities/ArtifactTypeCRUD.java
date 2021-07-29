package unit.entities;

import static org.assertj.core.api.Assertions.assertThat;

import java.io.Serializable;

import edu.nd.crc.safa.entities.ArtifactType;
import edu.nd.crc.safa.entities.Project;

import org.junit.jupiter.api.Test;

/* Tests that ArtifactTypes can be created
 *
 */
public class ArtifactTypeCRUD extends EntityBaseTest {
    @Test
    public void createRetrieveUpdateDeleteArtifactType() {
        String projectName = "test_project";
        String artifactTypeName = "Design Definitions";
        String altArtifactTypeName = "Requirements";

        Serializable projectId = createProject(projectName);
        Project project = session.find(Project.class, projectId);

        //VP 1 - Create Artifact Type
        ArtifactType artifactType = new ArtifactType(project, artifactTypeName);
        Serializable artifactTypeId = session.save(artifactType);
        assertThat(artifactTypeId).isNotNull();

        //VP 2 - Retrieve Artifact Type
        ArtifactType queriedArtifactType = session.find(ArtifactType.class, artifactTypeId);

        assertThat(queriedArtifactType).isNotNull();
        assertThat(queriedArtifactType.getName()).isEqualTo(artifactTypeName.toLowerCase());

        //VP 3 - Update Artifact Type
        queriedArtifactType.setName(altArtifactTypeName);
        session.update(queriedArtifactType);
        queriedArtifactType = session.find(ArtifactType.class, artifactTypeId);
        assertThat(queriedArtifactType.getName()).isEqualTo(altArtifactTypeName.toLowerCase());

        //VP 4 - Delete Artifact Type
        session.delete(queriedArtifactType);
        assertThat(session.find(ArtifactType.class, artifactTypeId)).isNull();
    }
}
