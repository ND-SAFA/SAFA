package features.matrices.base;

import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.repositories.TraceMatrixRepository;

import org.springframework.beans.factory.annotation.Autowired;
import features.base.ApplicationBaseTest;

/**
 * Tests that projects defined in database are to be retrieved by user.
 */
public abstract class AbstractMatrixTest extends ApplicationBaseTest {

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
