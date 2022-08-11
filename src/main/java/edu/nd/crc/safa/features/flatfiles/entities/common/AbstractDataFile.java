package edu.nd.crc.safa.features.flatfiles.entities.common;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;

import lombok.Data;
import org.javatuples.Pair;
import org.springframework.web.multipart.MultipartFile;

/**
 * Baseline functionality for parsing and validating artifacts.
 *
 * @param <E> The type of entities in data file (e.g. artifacts or traces)
 * @param <I> The type of record this file is handling.
 */
@Data
public abstract class AbstractDataFile<E, I> implements IDataFile<E>, IFlatFileParser {
    /**
     * Rows in csv file representing artifacts.
     */
    protected List<I> artifactRecords;
    /**
     * Entities parsed from file.
     */
    protected List<E> entities;
    /**
     * List of errors created while parsing entities.
     */
    protected List<String> errors;

    protected AbstractDataFile() {
        this.artifactRecords = new ArrayList<>();
        this.entities = new ArrayList<>();
        this.errors = new ArrayList<>();
    }

    protected AbstractDataFile(List<E> entities) {
        this();
        this.entities = entities;
    }

    protected AbstractDataFile(String pathToFile) throws IOException {
        this(pathToFile, true);
    }

    protected AbstractDataFile(String pathToFile, boolean parseOnConstructor) throws IOException {
        this();
        this.artifactRecords = readFileRecords(pathToFile);
        if (parseOnConstructor) {
            this.parseEntities();
        }
    }

    protected AbstractDataFile(MultipartFile file, boolean parseOnConstructor) throws IOException {
        this();
        this.artifactRecords = readFileRecords(file);
        if (parseOnConstructor) {
            this.parseEntities();
        }
    }

    @Override
    public void parseEntities() {
        this.entities = new ArrayList<>();
        this.errors = new ArrayList<>();
        for (I artifactRecord : artifactRecords) {
            Pair<E, String> response = this.parseRecord(artifactRecord);
            E entity = response.getValue0();
            String error = response.getValue1();
            if (error == null) {
                this.entities.add(entity);
            } else {
                this.errors.add(error);
            }
        }

        // Filters out invalid artifacts
        Pair<List<E>, List<String>> validationResponse = this.validateEntitiesCreated();
        this.entities = validationResponse.getValue0();
        this.errors = validationResponse.getValue1();
    }

    @Override
    public void export(File file) throws IOException {
        exportAsFileContent(file);
    }

    /**
     * Validates given entities and returns any errors found.
     *
     * @param projectAppEntity The entities existing in the system.
     * @return List of errors
     */
    public abstract Pair<List<E>, List<String>> validateInProject(ProjectAppEntity projectAppEntity);

    /**
     * Exports artifacts to given file.
     *
     * @param file The file to write entities to
     * @throws IOException If trouble reading objects, reading file, or writing to file.
     */
    protected abstract void exportAsFileContent(File file) throws IOException;

    /**
     * Keeps on valid entities and returns those with errors.
     *
     * @return List of erroneous entities and their errors
     */
    abstract Pair<List<E>, List<String>> validateEntitiesCreated();

    /**
     * Reads file in implemented format from path.
     */
    protected abstract List<I> readFileRecords(String pathToFile) throws IOException;

    /**
     * Reads MultipartFile in format.
     */
    protected abstract List<I> readFileRecords(MultipartFile file) throws IOException;

    /**
     * Parses record in file into an artifact
     *
     * @param entityRecord The artifact entry in the file.
     * @return The parsed artifact.
     */
    protected abstract Pair<E, String> parseRecord(I entityRecord);
}
