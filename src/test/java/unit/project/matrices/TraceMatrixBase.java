package unit.project.matrices;

import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.repositories.traces.TraceMatrixRepository;

import org.springframework.beans.factory.annotation.Autowired;
import unit.ApplicationBaseTest;

/**
 * Tests that projects defined in database are to be retrieved by user.
 */
public abstract class TraceMatrixBase extends ApplicationBaseTest {

    protected String sourceArtifactTypeName = "Requirements";
    protected String targetArtifactTypeName = "Design";
    protected String projectName = "test-project";

    @Autowired
    TraceMatrixRepository traceMatrixRepository;

    public Project createEmptyProject() {
        return dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newType(projectName, sourceArtifactTypeName)
            .newType(projectName, targetArtifactTypeName)
            .getProject(projectName);
    }
}
