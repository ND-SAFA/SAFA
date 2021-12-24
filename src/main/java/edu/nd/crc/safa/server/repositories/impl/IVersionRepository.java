package edu.nd.crc.safa.server.repositories.impl;

import java.util.List;

import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.EntityDelta;
import edu.nd.crc.safa.server.entities.app.IAppEntity;
import edu.nd.crc.safa.server.entities.db.CommitError;
import edu.nd.crc.safa.server.entities.db.IVersionEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

/**
 * Defines interface that all repositories related to versioned entities.
 *
 * @param <VersionEntity> The type of versioned entity.
 */
public interface IVersionRepository<
    VersionEntity extends IVersionEntity<AppEntity>,
    AppEntity extends IAppEntity> {

    /**
     * Returns the current entities existing in given project version.
     *
     * @param projectVersion The project version whose existing entities are retrieved.
     * @return List of entities in project version.
     */
    List<VersionEntity> getEntityVersionsInProjectVersion(ProjectVersion projectVersion);

    /**
     * Saves the state of given app entity to given project version.
     *
     * @param projectVersion The project version to save the changes to.
     * @param appEntity      The app entity whose state is saved.
     * @return String representing error message if one occurred.
     * @throws SafaError Throws error if saving changes fails.
     */
    CommitError commitSingleEntityToProjectVersion(ProjectVersion projectVersion, AppEntity appEntity) throws SafaError;

    /**
     * Saves given application entities to given version, saving removal entities for entities present in previous
     * versions but not present in given entities.
     *
     * @param projectVersion The project version whose changes are committed to.
     * @param appEntities    The app entities whose states are saved.
     * @return List of parsing errors occurring while saving app entities.
     * @throws SafaError Throws error if a fatal constraint or condition is not met.
     */
    List<CommitError> commitAllEntitiesInProjectVersion(ProjectVersion projectVersion,
                                                        List<AppEntity> appEntities) throws SafaError;

    /**
     * Deletes entity version with given name and commits to given project version.
     *
     * @param projectVersion The project version associated with committed removal.
     * @param baseEntityName The name of the base entity whose removal is committed to given version.
     * @return CommitError if error occurred while deleting entity, null otherwise.
     */
    CommitError deleteVersionEntityByBaseName(
        ProjectVersion projectVersion,
        String baseEntityName);

    /**
     * Calculates and returns the delta between the versions
     * beginning at base version and ending at target version.
     *
     * @param baselineVersion The starting version of the delta.
     * @param targetVersion   The ending version of the delta.
     * @return The change necessary to move between base and target version of artifact.
     */
    EntityDelta<AppEntity> calculateEntityDelta(ProjectVersion baselineVersion,
                                                ProjectVersion targetVersion);


    /**
     * @param versionEntity A versioned entity.
     * @return The corresponding app entity to given version entity.
     */
    AppEntity createAppFromVersion(VersionEntity versionEntity);
}
