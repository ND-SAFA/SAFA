package edu.nd.crc.safa.tgen.vsm;

import java.util.Collection;

/**
 * An interface defining a way of getting the similarity score between two lists
 * of artifacts.
 */
public interface ISimilarScoreCalculator {
    double getSimilarityScore(Collection<String> source, Collection<String> target);
}
