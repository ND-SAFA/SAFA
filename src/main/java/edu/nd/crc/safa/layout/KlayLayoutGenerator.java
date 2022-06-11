package edu.nd.crc.safa.layout;

import java.util.Hashtable;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.Getter;
import org.eclipse.elk.core.RecursiveGraphLayoutEngine;
import org.eclipse.elk.core.util.BasicProgressMonitor;
import org.eclipse.elk.graph.ElkGraphFactory;
import org.eclipse.elk.graph.ElkNode;

@Getter
public class KlayLayoutGenerator {
    public static final ElkGraphFactory factory = ElkGraphFactory.eINSTANCE;

    private final ElkNode graph;
    private final RecursiveGraphLayoutEngine graphLayoutEngine;
    private final BasicProgressMonitor progressMonitor;

    public KlayLayoutGenerator(
        List<ArtifactAppEntity> artifacts,
        List<TraceAppEntity> traces
    ) {
        this.graph = ElkGraphCreator.createGraphFromProject(artifacts, traces).getValue0();
        this.graphLayoutEngine = new RecursiveGraphLayoutEngine();
        this.progressMonitor = new BasicProgressMonitor();
    }

    /**
     * Runs layout algorithm on project artifacts and returns node.
     *
     * @return EkNode representing parent of all nodes (including islands).
     */
    public Map<String, Position> layout() {
        graphLayoutEngine.layout(graph, progressMonitor);
        Map<String, Position> positionMap = new Hashtable<>();
        addChildrenToMap(positionMap, graph);
        return positionMap;
    }

    private void addPositionToMap(Map<String, Position> map, ElkNode graph) {
        String id = graph.getIdentifier();
        if (!map.containsKey(id)) {
            Position graphPosition = new Position(graph.getX(), graph.getY());
            map.put(id, graphPosition);
            addChildrenToMap(map, graph);
        }
    }

    private void addChildrenToMap(Map<String, Position> map, ElkNode graph) {
        for (ElkNode child : graph.getChildren()) {
            addPositionToMap(map, child);
        }
    }

    @Data
    @AllArgsConstructor
    public static class Position {
        double x;
        double y;
    }
}
