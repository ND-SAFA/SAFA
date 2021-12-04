package edu.nd.crc.safa.server.repositories;

import java.util.Hashtable;
import java.util.List;

import edu.nd.crc.safa.server.entities.db.IEntityVersion;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

/**
 * Defines interface that all repositories related to versioned entities.
 *
 * @param <T> The type of versioned entity.
 */
public interface IVersionRepository<T extends IEntityVersion> {
    List<T> retrieveEntitiesAtProjectVersion(ProjectVersion projectVersion,
                                             Hashtable<String, List<T>> entitiesById);

}
