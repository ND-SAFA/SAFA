package edu.nd.crc.safa.features.traces.vsm;

/**
 * Defines an interface for a generic class able to create trace links.
 *
 * @param <E> The type identifying each traced entity.
 * @param <T> The type of link returned.
 */
public interface TraceLinkConstructor<E, T> {

    T createTraceLink(E source, E target, double score);
}
