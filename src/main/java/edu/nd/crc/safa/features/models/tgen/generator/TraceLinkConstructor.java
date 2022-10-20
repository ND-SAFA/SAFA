package edu.nd.crc.safa.features.models.tgen.generator;

/**
 * Defines an interface for a generic class able to create trace links.
 *
 * @param <E> The type identifying each traced entity.
 * @param <T> The type of link returned.
 */
public interface TraceLinkConstructor<E, T> {

    T createTraceLink(E source, E target, double score);
}
