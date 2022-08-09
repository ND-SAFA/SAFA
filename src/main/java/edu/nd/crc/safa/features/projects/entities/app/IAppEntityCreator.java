package edu.nd.crc.safa.features.projects.entities.app;

/**
 * Defines a lambda function for creating app entities from
 * a version entity.
 */
public interface IAppEntityCreator<A, V> {
    A createAppEntity(V v);
}
