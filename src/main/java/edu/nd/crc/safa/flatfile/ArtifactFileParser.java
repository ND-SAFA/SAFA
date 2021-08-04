package edu.nd.crc.safa.flatfile;

import java.io.IOException;
import java.util.Iterator;
import java.util.List;

import edu.nd.crc.safa.database.repositories.ArtifactBodyRepository;
import edu.nd.crc.safa.database.repositories.ArtifactFileRepository;
import edu.nd.crc.safa.database.repositories.ArtifactRepository;
import edu.nd.crc.safa.database.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.database.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.entities.Artifact;
import edu.nd.crc.safa.entities.ArtifactBody;
import edu.nd.crc.safa.entities.ArtifactFile;
import edu.nd.crc.safa.entities.ArtifactType;
import edu.nd.crc.safa.entities.Project;
import edu.nd.crc.safa.entities.ProjectVersion;
import edu.nd.crc.safa.output.error.ServerError;
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

    public void parseArtifactFiles(Project project,
                                   JSONObject dataFilesJson) throws JSONException, ServerError {
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

            ProjectVersion firstProjectVersion = new ProjectVersion(project);
            this.projectVersionRepository.save(firstProjectVersion);

            parseArtifactFile(project, firstProjectVersion, artifactType, artifactFileName);
        }
    }

    private void parseArtifactFile(Project project,
                                   ProjectVersion projectVersion,
                                   ArtifactType artifactType,
                                   String fileName) throws ServerError {

        CSVParser fileParser = FileUtilities.readCSVFile(project, fileName);
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
            ArtifactBody artifactBody = new ArtifactBody(artifact,
                projectVersion, artifactSummary, artifactContent);

            this.artifactRepository.save(artifact);
            this.artifactBodyRepository.save(artifactBody);
        }
    }


}
