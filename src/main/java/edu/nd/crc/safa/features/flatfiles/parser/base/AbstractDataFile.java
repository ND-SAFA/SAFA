package edu.nd.crc.safa.features.flatfiles.parser.base;

import java.io.File;
import java.io.IOException;
import java.nio.file.FileSystems;
import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.features.flatfiles.parser.interfaces.IDataFile;
import edu.nd.crc.safa.features.flatfiles.parser.interfaces.IFlatFileParser;
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
    private List<I> artifactRecords;
    /**
     * Entities parsed from file.
     */
    private List<E> entities;
    /**
     * List of errors created while parsing entities.
     */
    private List<String> errors;
    /**
     * The name of the file being parsed - used to generate more helpful error messages
     */
    private String filename;

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
        this.filename = FileSystems.getDefault().getPath(pathToFile).getFileName().toString();
        this.artifactRecords = tryReadFileRecords(() -> this.readFileRecords(pathToFile));
        if (parseOnConstructor) {
            this.parseEntities();
        }
    }

    protected AbstractDataFile(MultipartFile file, boolean parseOnConstructor) throws IOException {
        this();
        this.filename = file.getOriginalFilename();
        this.artifactRecords = tryReadFileRecords(() -> this.readFileRecords(file));
        if (parseOnConstructor) {
            this.parseEntities();
        }
    }

    /**
     * Try to read the file, and reformat the thrown exception if there is an issue with it.
     *
     * @param file The file object being parsed.
     * @return The records in the file.
     * @throws IOException If there is a problem with the file.
     */
    private List<I> tryReadFileRecords(ParsableFile<I> file) throws IOException {
        try {
            return file.parseFile();
        } catch (IOException e) {
            throw new IOException(String.format("%s: %s", filename, e.getMessage()), e);
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

    /**
     * Quick interface to wrap calls to readFileRecords so I don't have to duplicate code.
     * @param <I> The type of records in the file.
     */
    @FunctionalInterface
    private interface ParsableFile<I> {
        List<I> parseFile() throws IOException;
    }
}
