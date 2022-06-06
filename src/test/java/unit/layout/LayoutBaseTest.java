package unit.layout;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.junit.jupiter.api.BeforeEach;
import unit.ApplicationBaseTest;

public class LayoutBaseTest extends ApplicationBaseTest {

    String projectName = "test-project";
    ProjectVersion projectVersion;
    ProjectAppEntity project;

    @BeforeEach
    //TODO: Merge this with other before each
    public void setupDefaultProject() throws Exception {
        this.projectVersion = this.dbEntityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);
        uploadFlatFilesToVersion(projectVersion, ProjectPaths.PATH_TO_BEFORE_FILES);
        this.project = getProjectAtVersion(projectVersion);
    }
}
