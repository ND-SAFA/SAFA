package edu.nd.crc.safa.features.tgen;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;

/**
 * Determine which trace links are immediately visible.
 */
@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class LinkVisibilityService {

    private static final double TIER_ONE_THRESHOLD = 0.90; // 90-100 or top prediction above min score
    private static final double TOP_PARENT_MIN_SCORE = 0.75; // parent must reach SOME standard

    public static void setLinksVisibility(List<TraceAppEntity> links) {
        HashMap<String, List<TraceAppEntity>> child2links = createChildPredictionsMap(links);
        for (Map.Entry<String, List<TraceAppEntity>> entry : child2links.entrySet()) {

            List<TraceAppEntity> childLinks = entry.getValue();
            for (int i = 0; i < childLinks.size(); i++) {
                TraceAppEntity childLink = childLinks.get(i);
                double score = childLink.getScore();

                if (i == 0) {
                    if (score >= TOP_PARENT_MIN_SCORE) {
                        childLink.setVisible(true);
                    }
                } else if (score >= TIER_ONE_THRESHOLD) {
                    childLink.setVisible(true);
                }
            }
        }
    }

    private static HashMap<String, List<TraceAppEntity>> createChildPredictionsMap(List<TraceAppEntity> links) {
        HashMap<String, List<TraceAppEntity>> child2links = new HashMap<>();
        links.forEach(t -> {
            String childName = t.getSourceName();
            if (!child2links.containsKey(childName)) {
                child2links.put(childName, new ArrayList<>());
            }

            child2links.get(childName).add(t);
        });

        child2links.forEach((child, childLinks) -> {
            childLinks.sort(Comparator.comparingDouble(TraceAppEntity::getScore).reversed());
        });
        return child2links;
    }
}
