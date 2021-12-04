package edu.nd.crc.safa.server.repositories.impl;

import java.util.List;

import edu.nd.crc.safa.server.entities.app.IAppEntity;
import edu.nd.crc.safa.server.entities.db.IEntity;
import edu.nd.crc.safa.server.entities.db.IEntityVersion;
import edu.nd.crc.safa.server.entities.db.ModificationType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.utilities.ProjectVersionFilter;

/**
 * Defines interface that all repositories related to versioned entities.
 *
 * @param <VersionType> The type of versioned entity.
 */
public interface IVersionRepository<
    EntityType extends IEntity,
    VersionType extends IEntityVersion<AppType>,
    AppType extends IAppEntity> {
    List<VersionType> getEntitiesAtVersion(ProjectVersion projectVersion);

    List<VersionType> getEntitiesInProject(Project project);

    VersionType getLatestEntityVersionWithFilter(List<VersionType> bodies,
                                                 ProjectVersionFilter filter);

    ModificationType calculateModificationType(VersionType beforeBody,
                                               VersionType afterBody);

    List<VersionType> findByEntity(EntityType entity);

    VersionType getEntityAtVersion(List<VersionType> bodies, ProjectVersion version);

    VersionType getEntityBeforeVersion(List<VersionType> bodies, ProjectVersion version);

    ModificationType calculateModificationTypeForAppEntity(ProjectVersion projectVersion,
                                                           EntityType baseEntity,
                                                           AppType appEntity);
}
