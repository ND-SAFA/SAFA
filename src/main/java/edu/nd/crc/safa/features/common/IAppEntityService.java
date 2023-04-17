package edu.nd.crc.safa.features.common;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

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
     * @param user The user making the request
     * @return List of app entities
     */
    List<T> getAppEntities(ProjectVersion projectVersion, SafaUser user);

    default List<T> getAppEntitiesByIds(ProjectVersion projectVersion, SafaUser user, List<UUID> entityIds) {
        return this.getAppEntities(projectVersion, user)
            .stream()
            .filter(e -> entityIds.contains(e.getId()))
            .collect(Collectors.toList());
    }
}
