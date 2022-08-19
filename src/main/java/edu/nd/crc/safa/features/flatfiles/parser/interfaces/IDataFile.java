package edu.nd.crc.safa.features.flatfiles.parser.interfaces;

import java.io.File;
import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;

import org.javatuples.Pair;

/**
 * Defines interface for retrieving entities in artifact file.
 */
public interface IDataFile<E> {


    /**
     * Returns entities and errors created while creating the artifact file.
     *
     * @return Entities in data file alongside any parsing errors.
     */
    List<E> getEntities();

    /**
     * Returns list of parsing errors occurring when creating this data file.
     *
     * @return List of errors
     */
    List<String> getErrors();

    /**
     * Exports artifact file to give file.
     *
     * @param file The file to export entities to.
     */
    void export(File file) throws IOException;

    /**
     * Validates entities in data file against given project.
     *
     * @param projectAppEntity The project which the entities are validated against.
     * @return Pair of valid entities and list of strings representing validation messages.
     */
    Pair<List<E>, List<String>> validateInProject(ProjectAppEntity projectAppEntity);
}
