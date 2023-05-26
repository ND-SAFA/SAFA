package edu.nd.crc.safa.features.projects.graph;

import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Queue;
import java.util.Set;
import java.util.UUID;
import java.util.function.Function;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.common.ProjectEntities;
import edu.nd.crc.safa.features.projects.entities.app.SubtreeAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;

/**
 * <p>Calculates supertree and subtree sets for all artifacts in a project.</p>
 *
 * <p>This is similar to the calculations done in {@link ProjectGraph}, but this does
 * the full sub/super tree calculations, and it is all done in ID space so
 * no conversions have to be made when sending to the front end.</p>
 */
@NoArgsConstructor(access = AccessLevel.NONE)
public class SubtreeCalculator {

    /**
     * Calculates subtree entities based on the traces and artifacts in a project.
     *
     * @param entities Traces and artifacts in a project.
     * @return Calculated subtree information.
     */
    public static Map<UUID, SubtreeAppEntity> calculateSubtrees(ProjectEntities entities) {
        Map<UUID, SubtreeAppEntity> subtrees = generateSubtrees(entities.getArtifacts());
        calculateParents(subtrees, entities.getTraces());
        calculateTreeValues(subtrees);
        calculateNeighbors(subtrees);
        return subtrees;
    }

    /**
     * Generates empty subtree data for all artifacts in the project.
     *
     * @param artifacts Project artifacts.
     * @return One {@link SubtreeAppEntity} for each artifact in the list.
     */
    private static Map<UUID, SubtreeAppEntity> generateSubtrees(List<ArtifactAppEntity> artifacts) {
        Map<UUID, SubtreeAppEntity> subtrees = new HashMap<>();
        for (ArtifactAppEntity artifact : artifacts) {
            subtrees.put(artifact.getId(), new SubtreeAppEntity());
        }
        return subtrees;
    }

    /**
     * Calculates parent/children relationships from the list of traces and adds it to the subtree entity.
     *
     * @param subtrees Subtree entities we are in the process of building.
     * @param traces List of traces in the project.
     */
    private static void calculateParents(Map<UUID, SubtreeAppEntity> subtrees, List<TraceAppEntity> traces) {
        for (TraceAppEntity trace : traces) {
            UUID sourceId = trace.getSourceId();
            UUID targetId = trace.getTargetId();
            subtrees.get(sourceId).getParents().add(targetId);
            subtrees.get(targetId).getChildren().add(sourceId);
        }
    }

    /**
     * Calculates super- and subtree information based on the existing parent/child relationships
     * and updates the subtree entities.
     *
     * @param subtrees Subtree entities to add super- and subtree information into.
     */
    private static void calculateTreeValues(Map<UUID, SubtreeAppEntity> subtrees) {
        for (UUID item : subtrees.keySet()) {
            calculateSingleSubtree(item, subtrees);
            calculateSingleSupertree(item, subtrees);
        }
    }

    /**
     * Broadcasts this item into a supertree/subtree set all the way up/down its reachability chain.
     *
     * @param item Item we are processing.
     * @param subtrees Subtree information we are generating.
     * @param subtreeRetriever Function which will grab the supertree/subtree set from the app entity.
     * @param nextItemsRetriever Function which will grab the parent/children set from the app entity.
     */
    private static void broadcastTreeMembership(UUID item, Map<UUID, SubtreeAppEntity> subtrees,
                                                Function<SubtreeAppEntity, Set<UUID>> subtreeRetriever,
                                                Function<SubtreeAppEntity, Set<UUID>> nextItemsRetriever) {

        Queue<UUID> itemsToVisit = new LinkedList<>();
        itemsToVisit.add(item);

        Set<UUID> visited = new HashSet<>();

        while (!itemsToVisit.isEmpty()) {
            UUID currentItemId = itemsToVisit.poll();
            visited.add(currentItemId);

            SubtreeAppEntity currentItemInfo = subtrees.get(currentItemId);
            subtreeRetriever.apply(currentItemInfo).add(item);

            for (UUID nextId : nextItemsRetriever.apply(currentItemInfo)) {
                if (!visited.contains(nextId)) {
                    itemsToVisit.add(nextId);
                }
            }
        }

        subtreeRetriever.apply(subtrees.get(item)).remove(item);
    }

    /**
     * Calculates subtree information for this item by adding it to all of its ancestors' subtree sets.
     *
     * @param item The item we are processing.
     * @param subtrees The subtree information we are generating.
     */
    private static void calculateSingleSubtree(UUID item, Map<UUID, SubtreeAppEntity> subtrees) {
        broadcastTreeMembership(item, subtrees, SubtreeAppEntity::getSubtree, SubtreeAppEntity::getParents);
    }

    /**
     * Calculates supertree information for this item by adding it to all of its decendents' supertree sets.
     *
     * @param item The item we are processing.
     * @param subtrees The subtree information we are generating.
     */
    private static void calculateSingleSupertree(UUID item, Map<UUID, SubtreeAppEntity> subtrees) {
        broadcastTreeMembership(item, subtrees, SubtreeAppEntity::getSupertree, SubtreeAppEntity::getChildren);
    }

    /**
     * Calculates the neighbors of all items - which is just the combination of the supertree and subtree.
     *
     * @param subtrees The subtree information we're generating.
     */
    private static void calculateNeighbors(Map<UUID, SubtreeAppEntity> subtrees) {
        for (SubtreeAppEntity item : subtrees.values()) {
            item.getNeighbors().addAll(item.getSubtree());
            item.getNeighbors().addAll(item.getSupertree());
        }
    }
}
