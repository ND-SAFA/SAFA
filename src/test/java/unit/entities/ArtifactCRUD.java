package unit.entities;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.entities.Artifact;
import edu.nd.crc.safa.entities.ArtifactType;
import edu.nd.crc.safa.entities.Project;

import org.junit.jupiter.api.Test;

public class ArtifactCRUD extends EntityBaseTest {

    @Test
    public void createRetrieveUpdateDeleteArtifact() {
        String projectName = "test_project";
        UUID projectId = createProject(projectName);
        Project project = projectRepository.findByProjectId(projectId);

        String artifactTypeName = "design definitions";
        UUID artifactTypeId = createArtifactType(project, artifactTypeName);
        ArtifactType artifactType = artifactTypeRepository.findByTypeId(artifactTypeId);

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
