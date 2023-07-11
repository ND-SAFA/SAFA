package edu.nd.crc.safa.features.tgen.services;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.apache.commons.math3.stat.ranking.NaNStrategy;
import org.apache.commons.math3.stat.ranking.TiesStrategy;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class LinkScoreService {
    /**
     * Adjusts the link scores to represent the percentile in which each child ranked against the parent.
     *
     * @param links The links to adjust.
     */
    public static void convertLinksToPercentiles(List<TraceAppEntity> links) {
        HashMap<String, List<TraceAppEntity>> parent2links = LinkMapUtility.createParentMap(links);
        for (Map.Entry<String, List<TraceAppEntity>> entry : parent2links.entrySet()) {
            List<TraceAppEntity> parentLinks = entry.getValue();
            List<Double> scores = parentLinks.stream().map(TraceAppEntity::getScore).collect(Collectors.toList());
            double[] percentiles = scoresToPercentiles(scores);
            for (int i = 0; i < parentLinks.size(); i++) {
                parentLinks.get(i).setScore(percentiles[i]);
            }
        }
    }

    /**
     * Converts a list of scores to percentiles.
     *
     * @param scoreList The list scores whose rankings are converted.
     * @return List of percentiles.
     */
    private static double[] scoresToPercentiles(List<Double> scoreList) {
        PercentilesScaledRanking ranking = new PercentilesScaledRanking(NaNStrategy.REMOVED, TiesStrategy.MAXIMUM);
        double[] scores = scoreList.stream().mapToDouble(Double::doubleValue).toArray();
        return ranking.rank(scores);
    }
}

