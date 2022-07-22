package edu.nd.crc.safa.flatfiles;

import java.util.List;

import edu.nd.crc.safa.common.EntityCreation;
import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;

/**
 * Defines interface for parsing flat files of a certain format
 */
public interface IDataFile<E> {

    /**
     * Parses entities in file along and stores any errors.
     *
     * @return Entities created and errors encountered.
     */
    EntityCreation<E, String> parseEntities();

    /**
     * Validates given entities and returns any errors found.
     *
     * @param entities         The entities to validate.
     * @param projectAppEntity The entities existing in the system.
     * @return List of errors
     */
    List<String> validate(List<E> entities, ProjectAppEntity projectAppEntity);

    /**
     * Parses entities in file and validates them based on the given existing entities.
     *
     * @param projectAppEntity Entities in the existing project.
     * @return Entities created and errors encountered.
     */
    EntityCreation<E, String> parseAndValidateEntities(ProjectAppEntity projectAppEntity);
}
