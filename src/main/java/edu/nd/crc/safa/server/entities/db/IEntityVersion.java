package edu.nd.crc.safa.server.entities.db;

/**
 * Interface that generalizing similarities between all versioned entities.
 */
public interface IEntityVersion {

    ProjectVersion getProjectVersion();

    ModificationType getModificationType();

    String getEntityId();
}
