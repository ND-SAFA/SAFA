package edu.nd.crc.safa.test.features.projects.graph;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SubtreeAppEntity;
import edu.nd.crc.safa.features.projects.services.ProjectRetrievalService;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.traces.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.features.traces.entities.db.TraceType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

class TestSubtreeGeneration extends ApplicationBaseTest {

    @Autowired
    private ProjectRetrievalService projectRetrievalService;

    @Test
    void testSubtreeGeneration() {
        String typeName = "type";
        ProjectVersion version = dbEntityBuilder.newProject(projectName)
            .newType(projectName, typeName)
            .newVersionWithReturn(projectName);

        Artifact middle = dbEntityBuilder.newArtifactWithReturn(projectName, typeName, "middle");
        Artifact parent1 = dbEntityBuilder.newArtifactWithReturn(projectName, typeName, "parent1");
        Artifact parent2 = dbEntityBuilder.newArtifactWithReturn(projectName, typeName, "parent2");
        Artifact child1 = dbEntityBuilder.newArtifactWithReturn(projectName, typeName, "child1");
        Artifact child2 = dbEntityBuilder.newArtifactWithReturn(projectName, typeName, "child2");

        UUID middleId = middle.getArtifactId();
        UUID parent1Id = parent1.getArtifactId();
        UUID parent2Id = parent2.getArtifactId();
        UUID child1Id = child1.getArtifactId();
        UUID child2Id = child2.getArtifactId();

        dbEntityBuilder.newArtifactBody(projectName, 0, "middle", "", "")
            .newArtifactBody(projectName, 0, "parent1", "", "")
            .newArtifactBody(projectName, 0, "parent2", "", "")
            .newArtifactBody(projectName, 0, "child1", "", "")
            .newArtifactBody(projectName, 0, "child2", "", "");

        dbEntityBuilder.newTraceLink(projectName, child1.getName(), middle.getName(), 0)
            .newTraceLink(projectName, child2.getName(), middle.getName(), 0)
            .newTraceLink(projectName, middle.getName(), parent1.getName(), 0)
            .newTraceLink(projectName, middle.getName(), parent2.getName(), 0);

        TraceLinkVersion hiddenLink1 = dbEntityBuilder
            .newTraceLinkWithReturn(projectName, parent1.getName(), middle.getName(), 0);
        TraceLinkVersion hiddenLink2 = dbEntityBuilder
            .newTraceLinkWithReturn(projectName, parent2.getName(), middle.getName(), 0);

        hiddenLink1.setVisible(false);
        hiddenLink2.setTraceType(TraceType.GENERATED);
        hiddenLink2.setApprovalStatus(ApprovalStatus.DECLINED);
        traceLinkVersionRepository.saveAll(List.of(hiddenLink1, hiddenLink2));

        ProjectAppEntity project = projectRetrievalService.getProjectAppEntity(getCurrentUser(), version);
        Map<UUID, SubtreeAppEntity> subtrees = project.getSubtrees();

        assertEquals(5, subtrees.size());

        SubtreeAppEntity middleSubtree = subtrees.get(middleId);
        assertEquals(Set.of(parent1Id, parent2Id), middleSubtree.getParents());
        assertEquals(Set.of(parent1Id, parent2Id), middleSubtree.getSupertree());
        assertEquals(Set.of(child1Id, child2Id), middleSubtree.getChildren());
        assertEquals(Set.of(child1Id, child2Id), middleSubtree.getSubtree());
        assertEquals(Set.of(parent1Id, parent2Id, child1Id, child2Id), middleSubtree.getNeighbors());

        SubtreeAppEntity parent1Subtree = subtrees.get(parent1Id);
        assertEquals(Set.of(), parent1Subtree.getParents());
        assertEquals(Set.of(), parent1Subtree.getSupertree());
        assertEquals(Set.of(middleId), parent1Subtree.getChildren());
        assertEquals(Set.of(child1Id, child2Id, middleId), parent1Subtree.getSubtree());
        assertEquals(Set.of(child1Id, child2Id, middleId), parent1Subtree.getNeighbors());

        SubtreeAppEntity parent2Subtree = subtrees.get(parent2Id);
        assertEquals(Set.of(), parent2Subtree.getParents());
        assertEquals(Set.of(), parent2Subtree.getSupertree());
        assertEquals(Set.of(middleId), parent2Subtree.getChildren());
        assertEquals(Set.of(child1Id, child2Id, middleId), parent2Subtree.getSubtree());
        assertEquals(Set.of(child1Id, child2Id, middleId), parent2Subtree.getNeighbors());

        SubtreeAppEntity child1Subtree = subtrees.get(child1Id);
        assertEquals(Set.of(middleId), child1Subtree.getParents());
        assertEquals(Set.of(parent1Id, parent2Id, middleId), child1Subtree.getSupertree());
        assertEquals(Set.of(), child1Subtree.getChildren());
        assertEquals(Set.of(), child1Subtree.getSubtree());
        assertEquals(Set.of(parent1Id, parent2Id, middleId), child1Subtree.getNeighbors());

        SubtreeAppEntity child2Subtree = subtrees.get(child2Id);
        assertEquals(Set.of(middleId), child2Subtree.getParents());
        assertEquals(Set.of(parent1Id, parent2Id, middleId), child2Subtree.getSupertree());
        assertEquals(Set.of(), child2Subtree.getChildren());
        assertEquals(Set.of(), child2Subtree.getSubtree());
        assertEquals(Set.of(parent1Id, parent2Id, middleId), child2Subtree.getNeighbors());
    }
}
