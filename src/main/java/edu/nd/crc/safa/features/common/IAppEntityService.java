package edu.nd.crc.safa.features.common;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

/**
 * Defines interface with an app entity service. This includes:
 * - artifacts
 * - traces
 * - documents
 *
 * @param <T> The app entity type.
 */
public interface IAppEntityService<T extends IAppEntity> {

    /**
     * Retrieves and constructs app entities in given project version.
     *
     * @param projectVersion The version of the entities to construct.
     * @param user           The user making the request
     * @return List of app entities
     */
    List<T> getAppEntities(ProjectVersion projectVersion, SafaUser user);

    /**
     * Retrieves the app entities with given ids if present in project version.
     *
     * @param projectVersion The project version of the entities to calculate.
     * @param user           The user associated accessing entities.
     * @param appEntityIds   The IDs of the app entities to retrieve.
     * @return List of app entities.
     */
    List<T> getAppEntitiesByIds(ProjectVersion projectVersion, SafaUser user, List<UUID> appEntityIds);
}
