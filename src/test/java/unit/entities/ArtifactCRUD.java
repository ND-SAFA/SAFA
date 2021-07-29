package unit.entities;

import static org.assertj.core.api.Assertions.assertThat;

import java.io.Serializable;

import edu.nd.crc.safa.entities.Artifact;
import edu.nd.crc.safa.entities.ArtifactType;
import edu.nd.crc.safa.entities.Project;

import org.junit.jupiter.api.Test;

public class ArtifactCRUD extends EntityBaseTest {

    @Test
    public void createRetrieveUpdateDeleteArtifact() {
        String projectName = "test_project";
        Serializable projectId = createProject(projectName);
        Project project = session.find(Project.class, projectId);

        String artifactTypeName = "design definitions";
        Serializable artifactTypeId = createArtifactType(project, artifactTypeName);
        ArtifactType artifactType = session.find(ArtifactType.class, artifactTypeId);

        //VP 1 - Create artifact
        String artifactName = "RE-8";
        Artifact artifact = new Artifact(project, artifactType, artifactName);
        Serializable artifactId = session.save(artifact);

        //VP 2 - Retrieve artifact
        Artifact queriedArtifact = session.find(Artifact.class, artifactId);
        assertThat(queriedArtifact.getName()).isEqualTo(artifactName);
        assertThat(queriedArtifact.getType().getTypeId()).isEqualTo(artifactType.getTypeId());
    }
}
