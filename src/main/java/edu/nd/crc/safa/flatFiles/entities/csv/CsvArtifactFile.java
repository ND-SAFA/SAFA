package edu.nd.crc.safa.flatFiles.entities.csv;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;

import edu.nd.crc.safa.flatFiles.entities.AbstractArtifactFile;
import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.db.DocumentType;

import org.apache.commons.csv.CSVRecord;
import org.javatuples.Pair;
import org.springframework.web.multipart.MultipartFile;

/**
 * Reads artifacts from a CSV file.
 */
public class CsvArtifactFile extends AbstractArtifactFile<CSVRecord> {

    /**
     * The artifact type to be associated with all artifacts.
     */
    String artifactType;

    public CsvArtifactFile(String artifactType, String pathToFile) throws IOException {
        super(pathToFile);
        this.artifactType = artifactType;
    }

    public CsvArtifactFile(String artifactType, MultipartFile file) throws IOException {
        super(file);
        this.artifactType = artifactType;
    }

    @Override
    public List<String> validate(List newEntities, ProjectCommit projectCommit) {
        return new ArrayList<>();
    }

    @Override
    public List<CSVRecord> readFileRecords(String pathToFile) throws IOException {
        return CsvReader.readArtifactFile(pathToFile);
    }

    @Override
    public List<CSVRecord> readFileRecords(MultipartFile file) throws IOException {
        return CsvReader.readArtifactFile(file);
    }

    @Override
    public Pair<ArtifactAppEntity, String> parseRecord(CSVRecord entityRecord) {
        try {
            String artifactName = entityRecord.get(AbstractArtifactFile.Constants.NAME_PARAM);
            String artifactSummary = entityRecord.get(AbstractArtifactFile.Constants.SUMMARY_PARAM);
            String artifactContent = entityRecord.get(AbstractArtifactFile.Constants.CONTENT_PARAM);

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
}
