package edu.nd.crc.safa.tgen;

/**
 * Defines an interface for a generic class able to create trace links.
 *
 * @param <Key>   The type used to identify each entity traced.
 * @param <Value> The type of link returned.
 */
public interface TraceLinkConstructor<Key, Value> {

    Value createTraceLink(Key source, Key target, double score);
}
