package edu.nd.crc.safa.server.repositories.artifacts;

import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.delta.EntityDelta;
import edu.nd.crc.safa.server.entities.app.project.IAppEntity;
import edu.nd.crc.safa.server.entities.db.CommitError;
import edu.nd.crc.safa.server.entities.db.IVersionEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

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
     * Returns the version of the entity specified by entity id in given project version.
     *
     * @param projectVersion The version of the entity to retrieve.
     * @param entityId       The id of the base entity whose version is being retrieved.
     * @return Optional of entity version at given project version.
     */
    Optional<V> findVersionEntityByProjectVersionAndBaseEntityId(ProjectVersion projectVersion,
                                                                 String entityId);

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
     * @param projectVersion The project version to save the changes to.
     * @param a              The app entity whose state is saved.
     * @return String representing error message if one occurred.
     * @throws SafaError Throws error if saving changes fails.
     */
    Pair<V, CommitError> commitAppEntityToProjectVersion(ProjectVersion projectVersion,
                                                         A a) throws SafaError;

    /**
     * Saves given application entities to given version, saving removal entities for entities present in previous
     * versions but not present in given entities.
     *
     * @param projectVersion The project version whose changes are committed to.
     * @param appEntities    The app entities whose states are saved.
     * @return List of parsing errors occurring while saving app entities.
     * @throws SafaError Throws error if a fatal constraint or condition is not met.
     */
    List<Pair<V, CommitError>> commitAllAppEntitiesToProjectVersion(
        ProjectVersion projectVersion,
        List<A> appEntities) throws SafaError;

    /**
     * Deletes entity version with given name and commits to given project version.
     *
     * @param projectVersion The project version associated with committed removal.
     * @param baseEntityName The name of the base entity whose removal is committed to given version.
     * @return CommitError if error occurred while deleting entity, null otherwise.
     */
    Pair<V, CommitError> deleteVersionEntityByBaseEntityId(
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
    EntityDelta<A> calculateEntityDelta(ProjectVersion baselineVersion,
                                        ProjectVersion targetVersion);
}
