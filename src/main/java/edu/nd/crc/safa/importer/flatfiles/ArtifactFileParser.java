package edu.nd.crc.safa.importer.flatfiles;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.db.CommitError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectParsingActivities;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.artifacts.ArtifactFileRepository;
import edu.nd.crc.safa.server.repositories.artifacts.ArtifactRepository;
import edu.nd.crc.safa.server.repositories.artifacts.ArtifactTypeRepository;
import edu.nd.crc.safa.server.repositories.CommitErrorRepository;
import edu.nd.crc.safa.server.services.EntityVersionService;
import edu.nd.crc.safa.utilities.FileUtilities;

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

    private final ArtifactFileRepository artifactFileRepository;
    private final ArtifactRepository artifactRepository;
    private final ArtifactTypeRepository artifactTypeRepository;
    private final CommitErrorRepository commitErrorRepository;

    private final String NAME_PARAM = "id";
    private final String SUMMARY_PARAM = "summary";
    private final String CONTENT_PARAM = "content";
    private final String[] REQUIRED_COLUMNS = new String[]{NAME_PARAM, SUMMARY_PARAM, CONTENT_PARAM};
    EntityVersionService entityVersionService;

    @Autowired
    public ArtifactFileParser(ArtifactFileRepository artifactFileRepository,
                              ArtifactRepository artifactRepository,
                              ArtifactTypeRepository artifactTypeRepository,
                              EntityVersionService entityVersionService,
                              CommitErrorRepository commitErrorRepository) {
        this.artifactFileRepository = artifactFileRepository;
        this.artifactRepository = artifactRepository;
        this.artifactTypeRepository = artifactTypeRepository;
        this.entityVersionService = entityVersionService;
        this.commitErrorRepository = commitErrorRepository;
    }

    public List<ArtifactAppEntity> parseArtifactFiles(ProjectVersion projectVersion,
                                                      JSONObject dataFilesJson)
        throws JSONException, SafaError {

        List<ArtifactAppEntity> projectArtifacts = new ArrayList<>();
        for (Iterator<String> keyIterator = dataFilesJson.keys(); keyIterator.hasNext(); ) {
            String artifactTypeName = keyIterator.next();

            JSONObject artifactDefinitionJson = dataFilesJson.getJSONObject(artifactTypeName);
            if (!artifactDefinitionJson.has("file")) {
                throw new SafaError("Could not find key [file] in json: " + artifactDefinitionJson);
            }

            String artifactFileName = artifactDefinitionJson.getString("file");

            List<ArtifactAppEntity> artifacts = parseArtifactFile(projectVersion,
                artifactTypeName,
                artifactFileName);

            projectArtifacts.addAll(artifacts);
        }
        return projectArtifacts;
    }

    private List<ArtifactAppEntity> parseArtifactFile(ProjectVersion projectVersion,
                                                      String artifactType,
                                                      String fileName) throws SafaError {
        Project project = projectVersion.getProject();
        String pathToFile = ProjectPaths.getPathToFlatFile(project, fileName);
        CSVParser fileParser = FileUtilities.readCSVFile(pathToFile);

        List<ArtifactAppEntity> artifacts = parseArtifactFileIntoApplicationEntities(
            fileName,
            artifactType,
            fileParser);

        return artifacts;
    }

    public List<ArtifactAppEntity> parseArtifactFileIntoApplicationEntities(
        String fileName,
        String artifactType,
        CSVParser parsedFile) throws SafaError {
        List<CSVRecord> artifactRecords;
        try {
            artifactRecords = parsedFile.getRecords();
        } catch (IOException e) {
            throw new SafaError("Unable to read artifact file: " + fileName);
        }

        List<ArtifactAppEntity> artifactAppEntities = new ArrayList<>();
        for (CSVRecord artifactRecord : artifactRecords) {
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
                artifactContent
            );
            artifactAppEntities.add(artifactAppEntity);
        }

        return artifactAppEntities;
    }

    public CSVParser readArtifactFile(MultipartFile file) throws SafaError {
        return FileUtilities.readMultiPartCSVFile(file, REQUIRED_COLUMNS);
    }

    public Pair<List<ArtifactAppEntity>, List<CommitError>> validateArtifacts(ProjectVersion projectVersion,
                                                                              List<ArtifactAppEntity> artifacts) {
        List<String> errors = new ArrayList<>();
        List<ArtifactAppEntity> validArtifacts = new ArrayList<>();

        Hashtable<String, ArtifactAppEntity> artifactHashtable = new Hashtable<>();
        for (ArtifactAppEntity a : artifacts) {
            if (artifactHashtable.containsKey(a.name)) {
                errors.add("Found duplicate artifact: " + a.name);
            } else {
                artifactHashtable.put(a.name, a);
                validArtifacts.add(a);
            }
        }

        List<CommitError> commitErrors = errors
            .stream()
            .map(e -> new CommitError(projectVersion, e, ProjectParsingActivities.PARSING_ARTIFACTS))
            .collect(Collectors.toList());
        return new Pair<>(validArtifacts, commitErrors);
    }
}
