package edu.nd.crc.safa.importer.flatfiles;

import static edu.nd.crc.safa.importer.flatfiles.ProjectTIMParser.FILE_PARAM;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;

import edu.nd.crc.safa.common.EntityCreation;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.db.DocumentType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.utilities.FileUtilities;

import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import org.springframework.web.multipart.MultipartFile;

/**
 * Responsible for reading and parsing artifact files.
 */
public class ArtifactFile {
    public static String NAME_PARAM = "id";
    public static String SUMMARY_PARAM = "summary";
    public static String CONTENT_PARAM = "content";
    private static final String[] REQUIRED_COLUMNS = new String[]{NAME_PARAM, SUMMARY_PARAM, CONTENT_PARAM};
    public static String[] REQUIRED_KEYS = {FILE_PARAM};

    String name;
    String file;

    public ArtifactFile(String name, String file) {
        this.name = name;
        this.file = file;
    }

    public static EntityCreation<ArtifactAppEntity, String> parseArtifactFileIntoApplicationEntities(
        String artifactType,
        String file,
        CSVParser parsedFile) throws SafaError {
        List<CSVRecord> artifactRecords;
        try {
            artifactRecords = parsedFile.getRecords();
        } catch (IOException e) {
            throw new SafaError("Unable to read artifact file: " + file);
        }

        List<ArtifactAppEntity> artifactAppEntities = new ArrayList<>();
        List<String> errors = new ArrayList<>();
        for (CSVRecord artifactRecord : artifactRecords) {
            try {
                String artifactName = artifactRecord.get(NAME_PARAM);
                String artifactSummary = artifactRecord.get(SUMMARY_PARAM);
                String artifactContent = artifactRecord.get(CONTENT_PARAM);

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
                artifactAppEntities.add(artifactAppEntity);
            } catch (Exception e) {
                errors.add(e.getMessage());
            }
        }

        return new EntityCreation<>(artifactAppEntities, errors);
    }

    public static CSVParser readArtifactFile(MultipartFile file) throws SafaError {
        return FileUtilities.readMultiPartCSVFile(file, REQUIRED_COLUMNS);
    }

    public EntityCreation<ArtifactAppEntity, String> parseArtifacts(ProjectVersion projectVersion) throws SafaError {
        Project project = projectVersion.getProject();
        String pathToFile = ProjectPaths.getPathToFlatFile(project, this.file);
        CSVParser fileParser = FileUtilities.readCSVFile(pathToFile);
        return parseArtifactFileIntoApplicationEntities(this.name, this.file, fileParser);
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getFile() {
        return file;
    }

    public void setFile(String file) {
        this.file = file;
    }
}
