package edu.nd.crc.safa.test.features.layout.logic;

import edu.nd.crc.safa.features.layout.entities.app.LayoutPosition;
import edu.nd.crc.safa.features.layout.entities.db.ArtifactPosition;
import edu.nd.crc.safa.features.layout.repositories.ArtifactPositionRepository;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.test.features.layout.base.AbstractCorrectnessTest;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Tests that nodes are formatted in a hierarchical structure.
 */
class TestLayoutCorrectness extends AbstractCorrectnessTest {

    @Autowired
    ArtifactPositionRepository artifactPositionRepository;

    @Test
    void testParentWithTwoChildren() throws Exception {
        // Step - Create project
        createProject();

        Iterable<ArtifactPosition> artifactPositionRepositoryList = artifactPositionRepository.findAll();

        // Step - Create layout
        ProjectAppEntity project = retrievalService.getProjectAtVersion(projectVersion);

        // Step - Extract positions
        LayoutPosition a1Pos = getPosition(project, a1Name);
        LayoutPosition a2Pos = getPosition(project, a2Name);
        LayoutPosition a3Pos = getPosition(project, a3Name);

        // VP - Verify that root has greatest y
        assertLayoutCorrectness(a1Pos, a2Pos, a3Pos);
    }
}
