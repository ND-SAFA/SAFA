package edu.nd.crc.safa.features.generation.tgen.services;

import org.apache.commons.math3.stat.ranking.NaNStrategy;
import org.apache.commons.math3.stat.ranking.NaturalRanking;
import org.apache.commons.math3.stat.ranking.TiesStrategy;

/**
 * Calculates percentiles from ranking scores.
 */
public class PercentilesScaledRanking extends NaturalRanking {

    public PercentilesScaledRanking(NaNStrategy nanStrategy, TiesStrategy tiesStrategy) {
        super(nanStrategy, tiesStrategy);
    }

    /**
     * Calculates the percentiles from the ranks of the scores.
     *
     * @param scores List of scores defining rankings.
     * @return Percentiles of each score.
     */
    @Override
    public double[] rank(double[] scores) {
        double[] rank = super.rank(scores);
        for (int i = 0; i < rank.length; i++) {
            rank[i] = rank[i] / rank.length;
        }
        return rank;
    }
}
