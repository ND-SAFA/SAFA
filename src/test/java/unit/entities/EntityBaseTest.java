package unit.entities;

import java.io.Serializable;

import edu.nd.crc.safa.entities.ArtifactType;
import edu.nd.crc.safa.entities.Project;

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
        Project project = new Project();
        project.setName(projectName);
        return session.save(project);
    }

    public Serializable createArtifactType(Project project, String artifactTypeName) {
        ArtifactType artifactType = new ArtifactType();
        artifactType.setProject(project);
        artifactType.setName(artifactTypeName);
        return session.save(artifactType);
    }
}
