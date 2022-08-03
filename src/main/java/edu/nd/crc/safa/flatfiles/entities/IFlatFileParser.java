package edu.nd.crc.safa.flatfiles.entities;

/**
 * Interface for a parser of a flat file.
 *
 * @param <E> The type of entity created by this file.
 */
public interface IFlatFileParser<E> {
    /**
     * Parses entities in file along and stores any errors.
     */
    void parseEntities();
}
