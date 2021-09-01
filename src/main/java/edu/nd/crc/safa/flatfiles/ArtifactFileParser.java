package edu.nd.crc.safa.flatfiles;

import java.io.IOException;
import java.util.Iterator;
import java.util.List;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.entities.sql.Artifact;
import edu.nd.crc.safa.entities.sql.ArtifactBody;
import edu.nd.crc.safa.entities.sql.ArtifactFile;
import edu.nd.crc.safa.entities.sql.ArtifactType;
import edu.nd.crc.safa.entities.sql.Project;
import edu.nd.crc.safa.entities.sql.ProjectVersion;
import edu.nd.crc.safa.repositories.sql.ArtifactBodyRepository;
import edu.nd.crc.safa.repositories.sql.ArtifactFileRepository;
import edu.nd.crc.safa.repositories.sql.ArtifactRepository;
import edu.nd.crc.safa.repositories.sql.ArtifactTypeRepository;
import edu.nd.crc.safa.repositories.sql.ProjectVersionRepository;
import edu.nd.crc.safa.responses.ServerError;
import edu.nd.crc.safa.utilities.FileUtilities;

import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import org.json.JSONException;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/**
 * Responsible for parsing flat files including reading,
 * validating, and storing their data.
 */
@Component
public class ArtifactFileParser {

    private final String ID_PARAM = "id";
    private final String SUMMARY_PARAM = "summary";
    private final String CONTENT_PARAM = "content";
    private final String[] REQUIRED_COLUMNS = new String[]{ID_PARAM, SUMMARY_PARAM, CONTENT_PARAM};

    ArtifactFileRepository artifactFileRepository;
    ArtifactRepository artifactRepository;
    ArtifactBodyRepository artifactBodyRepository;
    ArtifactTypeRepository artifactTypeRepository;
    ProjectVersionRepository projectVersionRepository;

    @Autowired
    public ArtifactFileParser(ArtifactFileRepository artifactFileRepository,
                              ArtifactRepository artifactRepository,
                              ArtifactBodyRepository artifactBodyRepository,
                              ArtifactTypeRepository artifactTypeRepository,
                              ProjectVersionRepository projectVersionRepository) {
        this.artifactFileRepository = artifactFileRepository;
        this.artifactRepository = artifactRepository;
        this.artifactBodyRepository = artifactBodyRepository;
        this.artifactTypeRepository = artifactTypeRepository;
        this.projectVersionRepository = projectVersionRepository;
    }

    public void parseArtifactFiles(ProjectVersion projectVersion,
                                   JSONObject dataFilesJson) throws JSONException, ServerError {
        Project project = projectVersion.getProject();

        for (Iterator keyIterator = dataFilesJson.keys(); keyIterator.hasNext(); ) {
            String artifactTypeName = keyIterator.next().toString();

            JSONObject artifactDefinitionJson = dataFilesJson.getJSONObject(artifactTypeName);
            if (!artifactDefinitionJson.has("file")) {
                throw new ServerError("Could not find key [file] in json: " + artifactDefinitionJson);
            }

            String artifactFileName = artifactDefinitionJson.getString("file");

            ArtifactType artifactType = new ArtifactType(project, artifactTypeName);
            this.artifactTypeRepository.save(artifactType);

            ArtifactFile newFile = new ArtifactFile(project, artifactType, artifactFileName);
            this.artifactFileRepository.save(newFile);

            parseArtifactFile(projectVersion, artifactType, artifactFileName);
        }
    }

    private void parseArtifactFile(ProjectVersion projectVersion,
                                   ArtifactType artifactType,
                                   String fileName) throws ServerError {
        Project project = projectVersion.getProject();
        String pathToFile = ProjectPaths.getPathToFlatFile(project, fileName);
        CSVParser fileParser = FileUtilities.readCSVFile(pathToFile);
        FileUtilities.assertHasColumns(fileParser, REQUIRED_COLUMNS);

        ArtifactFile artifactFile = new ArtifactFile(project, artifactType, fileName);
        this.artifactFileRepository.save(artifactFile);

        saveArtifactRecords(project, projectVersion, artifactType, fileParser);
    }

    private void saveArtifactRecords(Project project,
                                     ProjectVersion projectVersion,
                                     ArtifactType artifactType,
                                     CSVParser parsedFile) throws ServerError {
        List<CSVRecord> artifactRecords;
        try {
            artifactRecords = parsedFile.getRecords();
        } catch (IOException e) {
            throw new ServerError("parsing artifact file", e);
        }

        for (CSVRecord artifactRecord : artifactRecords) {

            String artifactId = artifactRecord.get(ID_PARAM);
            String artifactSummary = artifactRecord.get(SUMMARY_PARAM);
            String artifactContent = artifactRecord.get(CONTENT_PARAM);

            Artifact artifact = new Artifact(project, artifactType, artifactId);
            ArtifactBody artifactBody = new ArtifactBody(
                projectVersion, artifact, artifactSummary, artifactContent);

            this.artifactRepository.save(artifact);
            this.artifactBodyRepository.save(artifactBody);
        }
    }
}
