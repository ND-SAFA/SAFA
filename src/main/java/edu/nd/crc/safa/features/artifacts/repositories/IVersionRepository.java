package edu.nd.crc.safa.features.artifacts.repositories;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.common.IVersionEntity;
import edu.nd.crc.safa.features.delta.entities.app.EntityDelta;
import edu.nd.crc.safa.features.errors.entities.db.CommitError;
import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.javatuples.Pair;

/**
 * Defines interface that all repositories related to versioned entities.
 *
 * @param <V> The type of versioned entity.
 */
public interface IVersionRepository<
    V extends IVersionEntity<A>,
    A extends IAppEntity> {

    /**
     * Returns the current entities existing in given project version.
     *
     * @param projectVersion The project version whose existing entities are retrieved.
     * @return List of entities in project version.
     */
    List<V> retrieveVersionEntitiesByProjectVersion(ProjectVersion projectVersion);

    /**
     * Returns the list of all application entities existing in given project version.
     *
     * @param projectVersion The version of the versioned entities to return.
     * @return List of application entities
     */
    List<A> retrieveAppEntitiesByProjectVersion(ProjectVersion projectVersion);

    /**
     * Returns the current entities existing in given project.
     *
     * @param project The project whose existing entities are retrieved.
     * @return List of entities in project version.
     */
    List<V> retrieveVersionEntitiesByProject(Project project);

    /**
     * Retrieves the version entities whose base ids are referenced in list.
     *
     * @param baseIds List of base entities to retrieve by.
     * @return List of versioned entities.
     */
    List<V> retrieveVersionEntitiesByBaseIds(List<UUID> baseIds);

    /**
     * Returns the version of the entity specified by entity id in given project version.
     *
     * @param projectVersion The version of the entity to retrieve.
     * @param entityId       The id of the base entity whose version is being retrieved.
     * @return Optional of entity version at given project version.
     */
    Optional<V> findVersionEntityByProjectVersionAndBaseEntityId(ProjectVersion projectVersion,
                                                                 UUID entityId);

    /**
     * Defines a method for constructing AppEntities for attaching sub-entities.
     *
     * @param v A versioned entity.
     * @return The corresponding app entity to given version entity.
     */
    A retrieveAppEntityFromVersionEntity(V v);

    /**
     * Saves the state of given app entity to given project version.
     *
     * @param projectVersion  The project version to save the changes to.
     * @param a               The app entity whose state is saved.
     * @param user            The user doing the update
     * @param entityHashTable A hash table of entities used to speed up retrieval.
     *                        See {@link #createVersionEntityMap(ProjectVersion, List)}
     * @return String representing error message if one occurred.
     * @throws SafaError Throws error if saving changes fails.
     */
    Pair<V, CommitError> commitAppEntityToProjectVersion(ProjectVersion projectVersion,
                                                         A a, SafaUser user,
                                                         Map<UUID, List<V>> entityHashTable) throws SafaError;

    /**
     * Saves given application entities to given version, saving removal entities for entities present in previous
     * versions but not present in given entities.
     *
     * @param projectVersion The project version whose changes are committed to.
     * @param appEntities    The app entities whose states are saved.
     * @param asCompleteSet  Whether entities create entire set of entities in project.
     * @param user           The user making the change
     * @return List of parsing errors occurring while saving app entities.
     * @throws SafaError Throws error if a fatal constraint or condition is not met.
     */
    List<Pair<V, CommitError>> commitAllAppEntitiesToProjectVersion(
        ProjectVersion projectVersion,
        List<A> appEntities,
        boolean asCompleteSet,
        SafaUser user) throws SafaError;

    /**
     * Deletes entity version with given name and commits to given project version.
     *
     * @param projectVersion  The project version associated with committed removal.
     * @param baseEntityName  The name of the base entity whose removal is committed to given version.
     * @param user            The user making the change
     * @param entityHashTable A hash table of entities used to speed up retrieval.
     *                        See {@link #createVersionEntityMap(ProjectVersion, List)}
     * @return CommitError if error occurred while deleting entity, null otherwise.
     */
    Pair<V, CommitError> deleteVersionEntityByBaseEntityId(
        ProjectVersion projectVersion,
        UUID baseEntityName,
        SafaUser user,
        Map<UUID, List<V>> entityHashTable);

    /**
     * Calculates and returns the delta between the versions
     * beginning at base version and ending at target version.
     *
     * @param baselineVersion The starting version of the delta.
     * @param targetVersion   The ending version of the delta.
     * @return The change necessary to move between base and target version of artifact.
     */
    EntityDelta<A> calculateEntityDelta(ProjectVersion baselineVersion,
                                        ProjectVersion targetVersion);

    /**
     * Update TIM related information as needed for a given entity update.
     *
     * @param projectVersion        The version the update is happening in
     * @param versionEntity         The newly updated entity
     * @param originalVersionEntity The previous version of the entity, if it exists (for calculating differences)
     * @param user                  The user doing the change
     */
    void updateTimInfo(ProjectVersion projectVersion, V versionEntity, V originalVersionEntity, SafaUser user);

    /**
     * Creates a map between entity ID and entity versions for all entities in the given project version.
     * Precalculating this information speeds up retrieval of entities, which in turn speeds up commits.
     *
     * @param projectVersion The version to retrieve entities from.
     * @param baseEntityIds  The ids of the base entities who have changed.
     * @return A map between entity ID and entity versions for all entities in the given project version.
     */
    Map<UUID, List<V>> createVersionEntityMap(ProjectVersion projectVersion, List<UUID> baseEntityIds);

    /**
     * Get the count of entities present in a particular project version
     *
     * @param projectVersion The version to check in
     * @return The number of entities in this version
     */
    int getCountInProjectVersion(ProjectVersion projectVersion);
}
