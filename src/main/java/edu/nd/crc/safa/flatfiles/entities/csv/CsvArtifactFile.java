package edu.nd.crc.safa.flatfiles.entities.csv;

import java.io.File;
import java.io.IOException;
import java.util.Hashtable;
import java.util.List;

import edu.nd.crc.safa.flatfiles.entities.AbstractArtifactFile;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.db.DocumentType;

import com.fasterxml.jackson.core.JsonProcessingException;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.apache.commons.csv.CSVRecord;
import org.javatuples.Pair;
import org.springframework.web.multipart.MultipartFile;

/**
 * A CSV file defining a set of artifacts on each row.
 * <p>
 * File is expected to contain a name, summary, and body
 */
public class CsvArtifactFile extends AbstractArtifactFile<CSVRecord> {

    /**
     * The artifact type to be associated with all artifacts.
     */
    String artifactType;

    public CsvArtifactFile(String artifactType, String pathToFile) throws IOException {
        super(pathToFile, false);
        setArtifactType(artifactType);
        this.parseEntities();
    }

    public CsvArtifactFile(String artifactType, MultipartFile file) throws IOException {
        super(file, false);
        setArtifactType(artifactType);
        this.parseEntities();
    }

    @Override
    protected void exportAsFileContent(File file) throws JsonProcessingException {
        // TODO: Convert entities into CSV rows
        // TODO: Write rows to file
    }

    @Override
    public List<CSVRecord> readFileRecords(String pathToFile) throws IOException {
        return CsvDataFileReader.readArtifactFile(pathToFile);
    }

    @Override
    public List<CSVRecord> readFileRecords(MultipartFile file) throws IOException {
        return CsvDataFileReader.readArtifactFile(file);
    }

    @Override
    public Pair<ArtifactAppEntity, String> parseRecord(CSVRecord entityRecord) {
        if (artifactType == null) {
            throw new IllegalArgumentException("Cannot parse record without artifact type");
        }
        try {
            String artifactName = entityRecord.get(Constants.NAME_PARAM);
            String artifactSummary = entityRecord.get(Constants.SUMMARY_PARAM);
            String artifactContent = entityRecord.get(Constants.CONTENT_PARAM);

            artifactSummary = artifactSummary == null ? "" : artifactSummary;
            artifactContent = artifactContent == null ? "" : artifactContent;
            ArtifactAppEntity artifactAppEntity = new ArtifactAppEntity(
                "",
                artifactType,
                artifactName,
                artifactSummary,
                artifactContent,
                DocumentType.ARTIFACT_TREE,
                new Hashtable<>()
            );
            return new Pair(artifactAppEntity, null);
        } catch (Exception e) {
            return new Pair<>(null, e.getMessage());
        }
    }

    public void setArtifactType(String artifactType) {
        if (artifactType == null) {
            throw new IllegalArgumentException("Artifact type cannot be null.");
        }
        this.artifactType = artifactType;
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Constants {
        public static final String NAME_PARAM = "id";
        public static final String SUMMARY_PARAM = "summary";
        public static final String CONTENT_PARAM = "content";
        public static final String[] REQUIRED_COLUMNS = new String[]{NAME_PARAM, SUMMARY_PARAM, CONTENT_PARAM};
    }
}
