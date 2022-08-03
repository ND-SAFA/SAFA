package edu.nd.crc.safa.flatfiles.entities;

/**
 * Interface for a parser of a flat file.
 */
public interface IFlatFileParser {
    /**
     * Parses entities in file along and stores any errors.
     */
    void parseEntities();
}
