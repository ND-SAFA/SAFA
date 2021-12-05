package edu.nd.crc.safa.server.repositories.impl;

import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.IAppEntity;
import edu.nd.crc.safa.server.entities.db.IBaseEntity;
import edu.nd.crc.safa.server.entities.db.IVersionEntity;
import edu.nd.crc.safa.server.entities.db.ModificationType;
import edu.nd.crc.safa.server.entities.db.ParserError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.utilities.ProjectVersionFilter;

import org.javatuples.Pair;

/**
 * Defines interface that all repositories related to versioned entities.
 *
 * @param <VersionEntity> The type of versioned entity.
 */
public interface IVersionRepository<
    BaseEntity extends IBaseEntity,
    VersionEntity extends IVersionEntity<AppEntity>,
    AppEntity extends IAppEntity> {
    List<VersionEntity> getEntityVersionsInProjectVersion(ProjectVersion projectVersion);

    List<VersionEntity> getEntitiesInProject(Project project);

    VersionEntity getLatestEntityVersionWithFilter(List<VersionEntity> bodies,
                                                   ProjectVersionFilter filter);

    ModificationType calculateModificationType(VersionEntity beforeBody,
                                               VersionEntity afterBody);

    List<VersionEntity> findByEntity(BaseEntity entity);

    VersionEntity getEntityAtVersion(List<VersionEntity> bodies, ProjectVersion version);

    VersionEntity getEntityBeforeVersion(List<VersionEntity> bodies, ProjectVersion version);

    ModificationType calculateModificationTypeForAppEntity(ProjectVersion projectVersion,
                                                           BaseEntity baseEntity,
                                                           AppEntity appEntity);

    VersionEntity createEntityVersionWithModification(ProjectVersion projectVersion,
                                                      ModificationType modificationType,
                                                      BaseEntity baseEntity,
                                                      AppEntity appEntity);

    Optional<VersionEntity> findEntityVersionInProjectVersion(ProjectVersion projectVersion,
                                                              BaseEntity baseEntity);

    VersionEntity calculateEntityVersionAtProjectVersion(ProjectVersion projectVersion,
                                                         BaseEntity artifact,
                                                         AppEntity appEntity);

    BaseEntity findOrCreateBaseEntityFromAppEntity(ProjectVersion projectVersion,
                                                   AppEntity artifactAppEntity);

    VersionEntity calculateEntityVersionAtProjectVersion(
        ProjectVersion projectVersion,
        AppEntity appEntity);

    void saveVersionEntity(VersionEntity artifactVersion) throws SafaError;

    void setAppEntityAtProjectVersion(ProjectVersion projectVersion, AppEntity artifact) throws SafaError;

    List<BaseEntity> getProjectBaseEntities(Project project);

    Pair<List<VersionEntity>, List<ParserError>> calculateApplicationEntitiesAtVersion(
        ProjectVersion projectVersion,
        List<AppEntity> projectArtifacts);

    List<ParserError> setAppEntitiesAtProjectVersion(ProjectVersion projectVersion,
                                                     List<AppEntity> appEntities) throws SafaError;
}
