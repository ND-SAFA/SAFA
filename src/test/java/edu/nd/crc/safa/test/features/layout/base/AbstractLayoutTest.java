package edu.nd.crc.safa.test.features.layout.base;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.layout.generator.ElkGraphCreator;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.FlatFileRequest;

import org.eclipse.elk.graph.ElkConnectableShape;
import org.eclipse.elk.graph.ElkEdge;
import org.eclipse.elk.graph.ElkNode;
import org.javatuples.Pair;
import org.junit.jupiter.api.BeforeEach;

/**
 * Base class responsible for:
 * 1. Creating default project
 * 2. Creating graph from project
 * 3. Filling out Hashtable
 */
public abstract class AbstractLayoutTest extends ApplicationBaseTest {

    protected ProjectVersion projectVersion;
    protected ProjectAppEntity projectAppEntity;
    protected ElkNode rootGraphNode;
    protected Map<UUID, ElkNode> name2nodes;

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
        FlatFileRequest.updateProjectVersionFromFlatFiles(projectVersion,
            ProjectPaths.Resources.Tests.DefaultProject.V1);
        this.projectAppEntity = retrievalService.getProjectAtVersion(projectVersion);
        Pair<ElkNode, Map<UUID, ElkNode>> response =
            ElkGraphCreator.createGraphFromProject(projectAppEntity.getArtifacts(), projectAppEntity.getTraces());
        rootGraphNode = response.getValue0();
        name2nodes = response.getValue1();
    }

    protected ElkNode getArtifact(String artifactName) {
        UUID artifactId = getArtifactId(artifactName);
        return name2nodes.get(artifactId);
    }

    protected UUID getArtifactId(String name) {
        return this.projectAppEntity
            .getArtifacts()
            .stream()
            .filter(a -> a.getName().equals(name))
            .collect(Collectors.toList())
            .get(0)
            .getId();
    }
}
