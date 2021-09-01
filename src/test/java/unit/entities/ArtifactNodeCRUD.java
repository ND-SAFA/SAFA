package unit.entities;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.Optional;

import edu.nd.crc.safa.entities.sql.Artifact;
import edu.nd.crc.safa.entities.sql.ArtifactType;
import edu.nd.crc.safa.entities.sql.Project;

import org.junit.jupiter.api.Test;
import unit.EntityBaseTest;

public class ArtifactNodeCRUD extends EntityBaseTest {

    @Test
    public void createRetrieveUpdateDeleteArtifact() {
        String projectName = "test_project";
        Project project = createProject(projectName);

        String artifactTypeName = "design definitions";
        ArtifactType artifactType = createArtifactType(project, artifactTypeName);

        //VP 1 - Create artifact
        String artifactName = "RE-8";
        Artifact artifact = new Artifact(project, artifactType, artifactName);
        artifactRepository.save(artifact);

        //VP 2 - Retrieve artifact
        Optional<Artifact> queriedArtifact = artifactRepository.findById(artifact.getArtifactId());
        assertThat(queriedArtifact.isPresent()).isTrue();
        Artifact artifactFound = queriedArtifact.get();
        assertThat(artifactFound.getName()).isEqualTo(artifactName);
        assertThat(artifactFound.getType().getTypeId()).isEqualTo(artifactType.getTypeId());
    }
}
