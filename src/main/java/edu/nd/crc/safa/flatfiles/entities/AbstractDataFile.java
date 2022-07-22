package edu.nd.crc.safa.flatfiles.entities;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.common.EntityCreation;
import edu.nd.crc.safa.flatfiles.IDataFile;
import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;

import lombok.Data;
import lombok.NoArgsConstructor;
import org.javatuples.Pair;
import org.springframework.web.multipart.MultipartFile;

/**
 * Baseline functionality for parsing and validating artifacts.
 *
 * @param <E> The type of entities in data file (e.g. artifacts or traces)
 * @param <R> The type of record this file is handling.
 */
@Data
@NoArgsConstructor
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

    @Override
    public EntityCreation<E, String> parseAndValidateEntities(ProjectAppEntity projectAppEntity) {
        EntityCreation<E, String> entityCreation = this.parseEntities();
        List<E> entities = entityCreation.getEntities();
        List<String> errors = this.validate(entities, projectAppEntity);
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
