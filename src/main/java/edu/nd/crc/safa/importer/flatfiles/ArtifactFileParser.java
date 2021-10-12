package edu.nd.crc.safa.importer.flatfiles;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.db.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.db.entities.sql.ArtifactFile;
import edu.nd.crc.safa.server.db.entities.sql.ArtifactType;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.db.repositories.ArtifactBodyRepository;
import edu.nd.crc.safa.server.db.repositories.ArtifactFileRepository;
import edu.nd.crc.safa.server.db.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.db.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.server.db.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.messages.ServerError;
import edu.nd.crc.safa.server.services.ArtifactService;
import edu.nd.crc.safa.utilities.FileUtilities;

import com.fasterxml.jackson.core.JsonProcessingException;
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

    ArtifactService artifactService;

    @Autowired
    public ArtifactFileParser(ArtifactFileRepository artifactFileRepository,
                              ArtifactRepository artifactRepository,
                              ArtifactBodyRepository artifactBodyRepository,
                              ArtifactTypeRepository artifactTypeRepository,
                              ProjectVersionRepository projectVersionRepository,
                              ArtifactService artifactService) {
        this.artifactFileRepository = artifactFileRepository;
        this.artifactRepository = artifactRepository;
        this.artifactBodyRepository = artifactBodyRepository;
        this.artifactTypeRepository = artifactTypeRepository;
        this.projectVersionRepository = projectVersionRepository;
        this.artifactService = artifactService;
    }

    public void parseArtifactFiles(ProjectVersion projectVersion,
                                   JSONObject dataFilesJson)
        throws JSONException, ServerError, JsonProcessingException {
        Project project = projectVersion.getProject();

        List<ArtifactAppEntity> projectArtifacts = new ArrayList<>();
        for (Iterator<String> keyIterator = dataFilesJson.keys(); keyIterator.hasNext(); ) {
            String artifactTypeName = keyIterator.next();

            JSONObject artifactDefinitionJson = dataFilesJson.getJSONObject(artifactTypeName);
            if (!artifactDefinitionJson.has("file")) {
                throw new ServerError("Could not find key [file] in json: " + artifactDefinitionJson);
            }

            String artifactFileName = artifactDefinitionJson.getString("file");

            ArtifactType artifactType = this.artifactTypeRepository
                .findByProjectAndNameIgnoreCase(project, artifactTypeName)
                .orElseGet(() -> new ArtifactType(project, artifactTypeName));
            this.artifactTypeRepository.save(artifactType);

            ArtifactFile newFile = new ArtifactFile(project, artifactType, artifactFileName);
            this.artifactFileRepository.save(newFile);

            List<ArtifactAppEntity> artifactsInFile = parseArtifactFile(projectVersion, artifactType, artifactFileName);
            projectArtifacts.addAll(artifactsInFile);
        }
        artifactService.setArtifactsAtVersion(projectVersion, projectArtifacts);
    }

    private List<ArtifactAppEntity> parseArtifactFile(ProjectVersion projectVersion,
                                                      ArtifactType artifactType,
                                                      String fileName) throws ServerError {
        Project project = projectVersion.getProject();
        String pathToFile = ProjectPaths.getPathToFlatFile(project, fileName);
        CSVParser fileParser = FileUtilities.readCSVFile(pathToFile);
        FileUtilities.assertHasColumns(fileParser, REQUIRED_COLUMNS);

        ArtifactFile artifactFile = new ArtifactFile(project, artifactType, fileName);
        this.artifactFileRepository.save(artifactFile);

        return saveOrUpdateArtifactRecords(project, projectVersion, artifactType, fileParser);
    }

    private List<ArtifactAppEntity> saveOrUpdateArtifactRecords(Project project,
                                                                ProjectVersion projectVersion,
                                                                ArtifactType artifactType,
                                                                CSVParser parsedFile) throws ServerError {
        List<CSVRecord> artifactRecords;
        try {
            artifactRecords = parsedFile.getRecords();
        } catch (IOException e) {
            throw new ServerError("parsing artifact file", e);
        }

        List<ArtifactAppEntity> artifactAppEntities = new ArrayList<>();
        for (CSVRecord artifactRecord : artifactRecords) {
            String artifactId = artifactRecord.get(ID_PARAM);
            String artifactSummary = artifactRecord.get(SUMMARY_PARAM);
            String artifactContent = artifactRecord.get(CONTENT_PARAM);

            ArtifactAppEntity artifactAppEntity = new ArtifactAppEntity(
                artifactType.getName(),
                artifactId,
                artifactSummary,
                artifactContent
            );
            artifactAppEntities.add(artifactAppEntity);
        }

        return artifactAppEntities;
    }
}
