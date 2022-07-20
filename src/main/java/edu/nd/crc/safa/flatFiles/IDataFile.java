package edu.nd.crc.safa.flatFiles;

import java.util.List;

import edu.nd.crc.safa.common.EntityCreation;
import edu.nd.crc.safa.server.entities.api.ProjectCommit;

/**
 * Defines interface for parsing flat files of a certain format
 */
public interface IDataFile<EntityType> {

    /**
     * Parses entities in file along and stores any errors.
     *
     * @return Entities created and errors encountered.
     */
    EntityCreation<EntityType, String> parseEntities();

    /**
     * Validates given entities and returns any errors found.
     *
     * @param entities      The entities to validate.
     * @param projectCommit The entities existing in the system.
     * @return List of errors
     */
    List<String> validate(List<EntityType> entities, ProjectCommit projectCommit);

    /**
     * Parses entities in file and validates them based on the given existing entities.
     *
     * @param projectCommit Entities in the existing project.
     * @return Entities created and errors encountered.
     */
    EntityCreation<EntityType, String> parseAndValidateEntities(ProjectCommit projectCommit);
}
