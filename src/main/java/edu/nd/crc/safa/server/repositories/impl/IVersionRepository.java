package edu.nd.crc.safa.server.repositories.impl;

import java.util.List;

import edu.nd.crc.safa.server.entities.db.IEntityVersion;
import edu.nd.crc.safa.server.entities.db.ModificationType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.utilities.ProjectVersionFilter;

/**
 * Defines interface that all repositories related to versioned entities.
 *
 * @param <T> The type of versioned entity.
 */
public interface IVersionRepository<T extends IEntityVersion> {
    List<T> getEntitiesAtVersion(ProjectVersion projectVersion);

    List<T> getEntitiesInProject(Project project);

    T getLatestEntityVersionWithFilter(List<T> bodies,
                                       ProjectVersionFilter filter);

    ModificationType calculateModificationType(T beforeBody,
                                               T afterBody);
}
