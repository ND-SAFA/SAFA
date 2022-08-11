package edu.nd.crc.safa.features.flatfiles.entities.common;

import java.io.File;
import java.io.IOException;
import java.util.List;

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
}
