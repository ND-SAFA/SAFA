package edu.nd.crc.safa.layout;

import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;

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

    public KlayLayoutGenerator(ProjectAppEntity projectAppEntity) {
        this.graph = ElkGraphCreator.createGraphFromProject(projectAppEntity).getValue0();
        this.graphLayoutEngine = new RecursiveGraphLayoutEngine();
        this.progressMonitor = new BasicProgressMonitor();
    }

    /**
     * Runs layout algorithm on project artifacts and returns node.
     *
     * @return EkNode representing parent of all nodes (including islands).
     */
    public ElkNode layout() {
        graphLayoutEngine.layout(graph, progressMonitor);
        return graph;
    }
}
