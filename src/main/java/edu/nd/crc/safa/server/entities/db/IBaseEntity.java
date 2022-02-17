package edu.nd.crc.safa.server.entities.db;

/**
 * The unique identifier representing an entity (e.g. artifact, trace link).
 * This object is used to link a series of versions associated with said entity.
 */
public interface IBaseEntity {
    String getBaseEntityId();
}
