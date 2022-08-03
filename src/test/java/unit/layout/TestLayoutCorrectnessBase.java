package unit.layout;

import edu.nd.crc.safa.layout.LayoutPosition;
import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;

import org.junit.jupiter.api.Test;

/**
 * Tests that nodes are formatted in a hierarchical structure.
 */
class TestLayoutCorrectnessBase extends CorrectnessBaseTest {

    @Test
    void testParentWithTwoChildren() throws Exception {
        // Step - Create project
        createProject();

        // Step - Create layout
        ProjectAppEntity project = getProjectAtVersion(projectVersion);

        // Step - Extract positions
        LayoutPosition a1Pos = getPosition(project, a1Name);
        LayoutPosition a2Pos = getPosition(project, a2Name);
        LayoutPosition a3Pos = getPosition(project, a3Name);

        // VP - Verify that root has greatest y
        assertLayoutCorrectness(a1Pos, a2Pos, a3Pos);
    }
}
