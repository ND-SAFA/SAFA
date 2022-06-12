package unit.layout;

import java.util.Hashtable;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.layout.ElkGraphCreator;
import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.eclipse.elk.graph.ElkNode;
import org.javatuples.Pair;
import org.junit.jupiter.api.BeforeEach;
import unit.ApplicationBaseTest;

/**
 * Base class responsible for:
 * 1. Creating default project
 * 2. Creating graph from project
 * 3. Filling out Hashtable
 */
public class LayoutBaseTest extends ApplicationBaseTest {

    String projectName = "test-project";
    ProjectVersion projectVersion;
    ProjectAppEntity project;
    ElkNode graph;
    Hashtable<String, ElkNode> name2nodes;

    @BeforeEach
    public void setupDefaultProject() throws Exception {
        this.projectVersion = this.dbEntityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);
        uploadFlatFilesToVersion(projectVersion, ProjectPaths.PATH_TO_DEFAULT_PROJECT);
        this.project = getProjectAtVersion(projectVersion);
        Pair<ElkNode, Hashtable<String, ElkNode>> response =
            ElkGraphCreator.createGraphFromProject(project.artifacts, project.traces);
        graph = response.getValue0();
        name2nodes = response.getValue1();
    }

    protected ElkNode getArtifact(String artifactName) {
        String artifactId = getArtifactId(artifactName);
        return name2nodes.get(artifactId);
    }

    protected String getArtifactId(String name) {
        return this.project
            .getArtifacts()
            .stream()
            .filter(a -> a.name.equals(name))
            .collect(Collectors.toList())
            .get(0)
            .id;
    }
}
