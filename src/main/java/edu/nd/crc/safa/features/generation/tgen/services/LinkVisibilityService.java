package edu.nd.crc.safa.features.generation.tgen.services;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;

/**
 * Determine which trace links are immediately visible.
 */
@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class LinkVisibilityService {
    /**
     * All links should be above a minimum threshold.
     * The next batch of links should be selected by children, allowing the next top links to be visible.
     */

    private static final double TIER_ONE_THRESHOLD = 0.9; // 90-100 or top prediction above min score

    /**
     * Selects the top links to make visible.
     *
     * @param links Generated links to select top links from.
     * @return List of modified links. Visible status is done in place.
     */
    public static List<TraceAppEntity> setLinksVisibility(List<TraceAppEntity> links) {
        links.forEach(t -> t.setVisible(false));
        HashMap<String, List<TraceAppEntity>> child2links = createPredictionMap(links);
        List<TraceAppEntity> finalLinks = new ArrayList<>();
        for (Map.Entry<String, List<TraceAppEntity>> entry : child2links.entrySet()) {
            List<TraceAppEntity> childLinks = entry.getValue();
            List<TraceAppEntity> selectedLinks = childLinks
                .stream()
                .filter(t -> t.getScore() >= TIER_ONE_THRESHOLD)
                .collect(Collectors.toList());
            if (selectedLinks.isEmpty() && !childLinks.isEmpty()) {
                TraceAppEntity topParent = childLinks.get(0);
                selectedLinks.add(topParent);
            }

            finalLinks.addAll(selectedLinks);
        }

        for (TraceAppEntity trace : finalLinks) {
            trace.setVisible(true);
        }
        return finalLinks;
    }

    private static HashMap<String, List<TraceAppEntity>> createPredictionMap(List<TraceAppEntity> links) {
        HashMap<String, List<TraceAppEntity>> child2links = LinkMapUtility.createChildLinkMap(links);
        child2links.forEach((child, childLinks) -> {
            childLinks.sort(Comparator.comparingDouble(TraceAppEntity::getScore).reversed());
        });
        return child2links;
    }
}
