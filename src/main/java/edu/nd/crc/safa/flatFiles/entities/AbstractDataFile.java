package edu.nd.crc.safa.flatFiles.entities;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.common.EntityCreation;
import edu.nd.crc.safa.flatFiles.IDataFile;
import edu.nd.crc.safa.server.entities.api.ProjectCommit;

import org.javatuples.Pair;
import org.springframework.web.multipart.MultipartFile;

public abstract class AbstractDataFile<E, R> implements IDataFile<E> {
    /**
     * Rows in csv file representing artifacts.
     */
    List<R> artifactRecords;

    protected AbstractDataFile(String pathToFile) throws IOException {
        this.artifactRecords = readFileRecords(pathToFile);
    }

    protected AbstractDataFile(MultipartFile file) throws IOException {
        this.artifactRecords = readFileRecords(file);
    }

    public EntityCreation<E, String> parseAndValidateEntities(ProjectCommit projectCommit) {
        EntityCreation<E, String> entityCreation = this.parseEntities();
        List<E> entities = entityCreation.getEntities();
        List<String> errors = this.validate(entities, projectCommit);
        return new EntityCreation<>(entities, errors);
    }

    @Override
    public EntityCreation<E, String> parseEntities() {
        List<E> artifactAppEntities = new ArrayList<>();
        List<String> errors = new ArrayList<>();
        for (R artifactRecord : artifactRecords) {
            Pair<E, String> response = this.parseRecord(artifactRecord);
            if (response.getValue1() == null) {
                artifactAppEntities.add(response.getValue0());
            } else {
                errors.add(response.getValue1());
            }
        }

        return new EntityCreation<>(artifactAppEntities, errors);
    }

    /**
     * Reads file in implemented format from path.
     */
    protected abstract List<R> readFileRecords(String pathToFile) throws IOException;

    /**
     * Reads MultipartFile in format.
     */
    protected abstract List<R> readFileRecords(MultipartFile file) throws IOException;

    /**
     * Parses record in file into an artifact
     *
     * @param entityRecord The artifact entry in the file.
     * @return The parsed artifact.
     */
    protected abstract Pair<E, String> parseRecord(R entityRecord);
}
