package unit.layout;

import edu.nd.crc.safa.layout.KlayLayoutGenerator;

import org.eclipse.elk.graph.ElkNode;
import org.junit.jupiter.api.Test;

public class TestPlayground extends LayoutBaseTest {

    @Test
    public void playground() {
        KlayLayoutGenerator layoutGenerator = new KlayLayoutGenerator(project);
        layoutGenerator.layout();
        System.out.println("Execution time:" + layoutGenerator.getProgressMonitor().getExecutionTime());

        printGraph(0, layoutGenerator.getGraph());
    }

    public void printGraph(int level, ElkNode node) {
        System.out.println(level + ":" + node);
        for (ElkNode child : node.getChildren()) {
            printGraph(level + 1, child);
        }
    }
}
