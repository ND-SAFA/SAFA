package edu.nd.crc.safa.server.entities.api;

/**
 * Defines a lambda for creating a generic object from a string;
 *
 * @param <ObjectType> The type of object that is created.
 */
public interface StringCreator<ObjectType> {
    ObjectType create(String content);
}
