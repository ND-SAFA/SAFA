package unit.layout;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.builders.requests.FlatFileRequest;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.layout.generator.ElkGraphCreator;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import org.eclipse.elk.graph.ElkConnectableShape;
import org.eclipse.elk.graph.ElkEdge;
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
public abstract class LayoutBaseTest extends ApplicationBaseTest {

    String projectName = "test-project";
    ProjectVersion projectVersion;
    ProjectAppEntity project;
    ElkNode rootGraphNode;
    Map<String, ElkNode> name2nodes;

    public static List<ElkNode> getChildren(ElkNode elkNode) {
        List<ElkNode> children = new ArrayList<>();
        for (ElkEdge edge : elkNode.getOutgoingEdges()) {
            List<ElkConnectableShape> targets = edge.getTargets();
            targets.forEach(t -> children.add((ElkNode) t));
        }
        return children;
    }

    public static ElkNode getParent(ElkNode elkNode) {
        //TODO : Guarantee certain parent is more than one
        for (ElkEdge edge : elkNode.getIncomingEdges()) {
            List<ElkConnectableShape> targets = edge.getSources();
            if (targets.size() > 0) {
                return (ElkNode) targets.get(0);
            }
        }
        return null;
    }

    @BeforeEach
    public void setupDefaultProject() throws Exception {
        this.projectVersion = this.dbEntityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);
        FlatFileRequest.updateProjectVersionFromFlatFiles(projectVersion, ProjectPaths.PATH_TO_DEFAULT_PROJECT);
        this.project = getProjectAtVersion(projectVersion);
        Pair<ElkNode, Map<String, ElkNode>> response =
            ElkGraphCreator.createGraphFromProject(project.artifacts, project.traces);
        rootGraphNode = response.getValue0();
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
