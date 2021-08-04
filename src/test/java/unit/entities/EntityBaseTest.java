package unit.entities;

import java.util.UUID;

import edu.nd.crc.safa.database.repositories.ArtifactRepository;
import edu.nd.crc.safa.database.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.database.repositories.ProjectRepository;
import edu.nd.crc.safa.entities.Artifact;
import edu.nd.crc.safa.entities.ArtifactType;
import edu.nd.crc.safa.entities.Project;

import org.springframework.beans.factory.annotation.Autowired;
import unit.SpringBootBaseTest;

public class EntityBaseTest extends SpringBootBaseTest {

    @Autowired
    ProjectRepository projectRepository;

    @Autowired
    ArtifactTypeRepository artifactTypeRepository;

    @Autowired
    ArtifactRepository artifactRepository;

    public UUID createProject(String projectName) {
        Project project = new Project(projectName);
        projectRepository.save(project);
        return project.getProjectId();
    }

    public UUID createArtifactType(Project project, String artifactTypeName) {
        ArtifactType artifactType = new ArtifactType(project, artifactTypeName);
        artifactTypeRepository.save(artifactType);
        return artifactType.getTypeId();
    }

    public UUID createArtifact(Project project, ArtifactType type, String name) {
        Artifact artifact = new Artifact(project, type, name);
        artifactRepository.save(artifact);
        return artifact.getArtifactId();
    }
}
