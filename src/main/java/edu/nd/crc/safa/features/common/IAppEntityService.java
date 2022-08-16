package edu.nd.crc.safa.features.common;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

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
     * @return List of app entities
     */
    List<T> getAppEntities(ProjectVersion projectVersion);

    default List<T> getAppEntitiesByIds(ProjectVersion projectVersion, List<String> entityIds) {
        return this.getAppEntities(projectVersion)
            .stream()
            .filter(e -> entityIds.contains(e.getBaseEntityId()))
            .collect(Collectors.toList());
    }
}
