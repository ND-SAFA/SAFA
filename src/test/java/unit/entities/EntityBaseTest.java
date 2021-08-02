package unit.entities;

import java.io.Serializable;

import edu.nd.crc.safa.database.entities.Artifact;
import edu.nd.crc.safa.database.entities.ArtifactType;
import edu.nd.crc.safa.database.entities.Project;

import org.hibernate.Session;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import unit.SpringBootBaseTest;

public class EntityBaseTest extends SpringBootBaseTest {
    Session session;

    @BeforeEach
    public void loadSession() {
        session = this.sessionFactory.openSession();
    }

    @AfterEach
    public void closeSession() {
        if (session != null) {
            session.close();
        }
    }

    public Serializable createProject(String projectName) {
        Project project = new Project(projectName);
        return session.save(project);
    }

    public Serializable createArtifactType(Project project, String artifactTypeName) {
        ArtifactType artifactType = new ArtifactType(project, artifactTypeName);
        return session.save(artifactType);
    }

    public Serializable createArtifact(Project project, ArtifactType type, String name) {
        Artifact artifact = new Artifact(project, type, name);
        return session.save(artifact);
    }
}
