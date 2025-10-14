package edu.nd.crc.safa.test.features.projects.graph;


import static org.assertj.core.api.Assertions.assertThat;

import java.util.HashSet;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.graph.ArtifactNode;
import edu.nd.crc.safa.features.projects.graph.ProjectGraph;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;

import org.junit.jupiter.api.Test;

/**
 * Constructs a project containing a parent with two children.
 * Verifies that ProjectGraph is constructed accurately.
 */
public class TestGraphConstruction extends ApplicationBaseTest {
    String projectName = "graph-construction";
    String typeOneName = "type-1";
    String typeTwoName = "type-2";
    String typeThreeName = "type-3";
    String artifactOneName = "artifact-1";
    String artifactTwoName = "artifact-2";
    String artifactThreeName = "artifact-3";

    private ProjectAppEntity constructProject() {
        ProjectVersion projectVersion = this.dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newType(projectName, typeOneName)
            .newType(projectName, typeTwoName)
            .newType(projectName, typeThreeName)
            .newArtifactAndBody(projectName, typeOneName, artifactOneName, "", "")
            .newArtifactAndBody(projectName, typeTwoName, artifactTwoName, "", "")
            .newArtifactAndBody(projectName, typeThreeName, artifactThreeName, "", "")
            .newTraceLink(projectName, artifactTwoName, artifactOneName, 0)
            .newTraceLink(projectName, artifactThreeName, artifactOneName, 0)
            .getProjectVersion(projectName, 0);
        return retrievalService.getProjectAtVersion(projectVersion);
    }

    /**
     * Tests that construction of graph is accurate.
     */
    @Test
    public void testConstruction() {
        ProjectAppEntity project = constructProject();
        ProjectGraph graph = new ProjectGraph(project);
        ArtifactNode nodeOne = getArtifactNode(project, graph, typeOneName);
        ArtifactNode nodeTwo = getArtifactNode(project, graph, typeTwoName);
        ArtifactNode nodeThree = getArtifactNode(project, graph, typeThreeName);

        assertThat(nodeOne.getNeighbors()).hasSize(2);
        assertThat(nodeOne.getParents()).isEmpty();
        assertThat(nodeOne.getChildren()).hasSize(2);

        assertThat(nodeTwo.getNeighbors()).hasSize(1);
        assertThat(nodeTwo.getParents()).hasSize(1);
        assertThat(nodeTwo.getChildren()).isEmpty();

        assertThat(nodeThree.getNeighbors()).hasSize(1);
        assertThat(nodeThree.getParents()).hasSize(1);
        assertThat(nodeThree.getChildren()).isEmpty();
    }

    /**
     * Tests that neighborhood calculate is accurate.
     */
    @Test
    public void testNeighborhood() {
        ProjectAppEntity project = constructProject();
        ProjectGraph graph = new ProjectGraph(project);
        ArtifactNode artifactNode = getArtifactNode(project, graph, typeTwoName);

        // VP - Verify correctness of edges
        assertThat(artifactNode.getChildren()).isEmpty();
        assertThat(artifactNode.getParents()).hasSize(1);

        // VP - No types = empty neighborhood
        List<UUID> emptyNeighborhood = artifactNode.getNeighborhoodWithTypes(new HashSet<>());
        assertThat(emptyNeighborhood).isEmpty();

        // VP - Correctness of calculation
        List<UUID> neighborhoodSingle = artifactNode.getNeighborhoodWithTypes(new HashSet<>(List.of(typeOneName)));
        assertThat(neighborhoodSingle).hasSize(1);

        // VP - Correctness of calculation (includes parent and sibling).
        List<UUID> neighborhoodMany = artifactNode.getNeighborhoodWithTypes(new HashSet<>(List.of(typeOneName,
            typeThreeName)));
        assertThat(neighborhoodMany).hasSize(2);
    }

    private ArtifactNode getArtifactNode(ProjectAppEntity project, ProjectGraph graph, String typeName) {
        ArtifactAppEntity artifact = project.getByArtifactType(typeName).get(0);
        return graph.getArtifactNode(artifact.getId());
    }
}
