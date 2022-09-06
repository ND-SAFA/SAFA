package edu.nd.crc.safa.features.layout.generator;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.layout.entities.app.LayoutPosition;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

import lombok.Getter;
import org.eclipse.elk.alg.mrtree.options.MrTreeMetaDataProvider;
import org.eclipse.elk.core.RecursiveGraphLayoutEngine;
import org.eclipse.elk.core.data.LayoutMetaDataService;
import org.eclipse.elk.core.util.BasicProgressMonitor;
import org.eclipse.elk.graph.ElkGraphFactory;
import org.eclipse.elk.graph.ElkNode;

@Getter
public class KlayLayoutGenerator {
    public static final ElkGraphFactory factory = ElkGraphFactory.eINSTANCE;
    private static final LayoutMetaDataService SERVICE = LayoutMetaDataService.getInstance();

    static {
        SERVICE.registerLayoutMetaDataProviders(new MrTreeMetaDataProvider());
    }

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
    public Map<UUID, LayoutPosition> layout() {
        progressMonitor.logGraph(graph, "start");
        graphLayoutEngine.layout(graph, progressMonitor);
        return createPositionMap();
    }

    private Map<UUID, LayoutPosition> createPositionMap() {
        Map<UUID, LayoutPosition> positionMap = new HashMap<>();
        addChildrenToPositionMap(positionMap, graph);
        return positionMap;
    }

    private void addChildrenToPositionMap(Map<UUID, LayoutPosition> map, ElkNode graph) {
        for (ElkNode child : graph.getChildren()) {
            addPositionToMap(map, child);
        }
    }

    private void addPositionToMap(Map<UUID, LayoutPosition> map, ElkNode graph) {
        UUID id = UUID.fromString(graph.getIdentifier());
        map.computeIfAbsent(id, newKey -> {
            LayoutPosition graphPosition = new LayoutPosition(graph.getX(), graph.getY());
            addChildrenToPositionMap(map, graph);
            return graphPosition;
        });
    }
}
