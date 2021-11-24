package edu.nd.crc.safa.importer.flatfiles;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.api.ServerError;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.db.ApplicationActivity;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactFile;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.ParserError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ArtifactBodyRepository;
import edu.nd.crc.safa.server.repositories.ArtifactFileRepository;
import edu.nd.crc.safa.server.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.server.repositories.ParserErrorRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.services.ArtifactVersionService;
import edu.nd.crc.safa.utilities.FileUtilities;

import com.fasterxml.jackson.core.JsonProcessingException;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import org.javatuples.Pair;
import org.json.JSONException;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.multipart.MultipartFile;

/**
 * Responsible for parsing flat files including reading,
 * validating, and storing their data.
 */
@Component
public class ArtifactFileParser {

    private final String NAME_PARAM = "id";
    private final String SUMMARY_PARAM = "summary";
    private final String CONTENT_PARAM = "content";
    private final String[] REQUIRED_COLUMNS = new String[]{NAME_PARAM, SUMMARY_PARAM, CONTENT_PARAM};

    ArtifactFileRepository artifactFileRepository;
    ArtifactRepository artifactRepository;
    ArtifactBodyRepository artifactBodyRepository;
    ArtifactTypeRepository artifactTypeRepository;
    ProjectVersionRepository projectVersionRepository;
    ParserErrorRepository parserErrorRepository;

    ArtifactVersionService artifactVersionService;

    @Autowired
    public ArtifactFileParser(ArtifactFileRepository artifactFileRepository,
                              ArtifactRepository artifactRepository,
                              ArtifactBodyRepository artifactBodyRepository,
                              ArtifactTypeRepository artifactTypeRepository,
                              ProjectVersionRepository projectVersionRepository,
                              ArtifactVersionService artifactVersionService,
                              ParserErrorRepository parserErrorRepository) {
        this.artifactFileRepository = artifactFileRepository;
        this.artifactRepository = artifactRepository;
        this.artifactBodyRepository = artifactBodyRepository;
        this.artifactTypeRepository = artifactTypeRepository;
        this.projectVersionRepository = projectVersionRepository;
        this.artifactVersionService = artifactVersionService;
        this.parserErrorRepository = parserErrorRepository;
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

            Pair<List<ArtifactAppEntity>, List<ParserError>> parseResponse = parseArtifactFile(projectVersion,
                artifactType,
                artifactFileName);

            projectArtifacts.addAll(parseResponse.getValue0());
            this.parserErrorRepository.saveAll(parseResponse.getValue1());
        }
        artifactVersionService.setArtifactsAtVersion(projectVersion, projectArtifacts);
    }

    private Pair<List<ArtifactAppEntity>, List<ParserError>> parseArtifactFile(ProjectVersion projectVersion,
                                                                               ArtifactType artifactType,
                                                                               String fileName) throws ServerError {
        Project project = projectVersion.getProject();
        String pathToFile = ProjectPaths.getPathToFlatFile(project, fileName);
        CSVParser fileParser = FileUtilities.readCSVFile(pathToFile);

        ArtifactFile artifactFile = new ArtifactFile(project, artifactType, fileName);
        this.artifactFileRepository.save(artifactFile);
        //TODO: Remove artifact file repository;

        Pair<List<ArtifactAppEntity>, List<String>> response = parseArtifactFileIntoApplicationEntities(
            projectVersion.getProject(),
            fileName,
            artifactType.getName(),
            fileParser);
        List<ParserError> parserErrors = response.getValue1().stream().map(msg -> new ParserError(projectVersion,
            msg, ApplicationActivity.PARSING_ARTIFACTS)).collect(Collectors.toList());
        return new Pair<>(response.getValue0(), parserErrors);
    }

    public Pair<List<ArtifactAppEntity>, List<String>> parseArtifactFileIntoApplicationEntities(
        Project project,
        String fileName,
        String artifactType,
        CSVParser parsedFile) {
        List<CSVRecord> artifactRecords = new ArrayList<>();
        List<String> errors = new ArrayList<>();
        try {
            artifactRecords = parsedFile.getRecords();
        } catch (IOException e) {
            String error = String.format("Unable to read records in file: %s", fileName);
            errors.add(error);
        }

        List<ArtifactAppEntity> artifactAppEntities = new ArrayList<>();
        for (CSVRecord artifactRecord : artifactRecords) {
            String artifactName = artifactRecord.get(NAME_PARAM);
            String artifactSummary = artifactRecord.get(SUMMARY_PARAM);
            String artifactContent = artifactRecord.get(CONTENT_PARAM);
            String artifactId = getArtifactIdIfExists(project, artifactName);

            artifactSummary = artifactSummary == null ? "" : artifactSummary;
            artifactContent = artifactContent == null ? "" : artifactContent;

            ArtifactAppEntity artifactAppEntity = new ArtifactAppEntity(
                artifactId,
                artifactType,
                artifactName,
                artifactSummary,
                artifactContent
            );
            artifactAppEntities.add(artifactAppEntity);
        }

        return new Pair<>(artifactAppEntities, errors);
    }

    private String getArtifactIdIfExists(Project project, String artifactName) {
        String artifactId = "";

        if (project != null) {
            Optional<Artifact> artifactQuery = artifactRepository.findByProjectAndName(project, artifactName);
            if (artifactQuery.isPresent()) {
                artifactId = artifactQuery.get().getArtifactId().toString();
            }
        }
        return artifactId;
    }

    public CSVParser readArtifactFile(MultipartFile file) throws ServerError {
        return FileUtilities.readMultiPartCSVFile(file, REQUIRED_COLUMNS);
    }
}
