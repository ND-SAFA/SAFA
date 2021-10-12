package edu.nd.crc.safa.importer.flatfiles;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.db.entities.sql.ArtifactType;
import edu.nd.crc.safa.server.db.entities.sql.ParserError;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.db.entities.sql.TraceLink;
import edu.nd.crc.safa.server.db.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.db.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.server.db.repositories.ParserErrorRepository;
import edu.nd.crc.safa.server.db.repositories.TraceLinkRepository;
import edu.nd.crc.safa.server.messages.ServerError;
import edu.nd.crc.safa.server.services.RevisionNotificationService;
import edu.nd.crc.safa.server.services.TraceLinkService;
import edu.nd.crc.safa.utilities.FileUtilities;

import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import org.javatuples.Pair;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/**
 * Responsible for parsing, validating, and creating trace links.
 *
 * <p>A TraceMatrixDefinition is a JSON object defining:
 * source: String - the name of the source artifact's type
 * target: String - the name of the target artifact's type
 * file: String - name of uploaded file containing the matrices links.
 *
 * <p>Such that the keys are in lower case.
 */
@Component
public class TraceFileParser {

    private final String SOURCE_PARAM = "source";
    private final String TARGET_PARAM = "target";
    private final String[] REQUIRED_COLUMNS = new String[]{SOURCE_PARAM, TARGET_PARAM};

    TraceLinkService traceLinkService;
    ArtifactRepository artifactRepository;
    ArtifactTypeRepository artifactTypeRepository;
    ParserErrorRepository parserErrorRepository;
    TraceLinkRepository traceLinkRepository;
    TraceLinkGenerator traceLinkGenerator;
    RevisionNotificationService revisionNotificationService;

    @Autowired
    public TraceFileParser(TraceLinkService traceLinkService,
                           ArtifactRepository artifactRepository,
                           ArtifactTypeRepository artifactTypeRepository,
                           ParserErrorRepository parserErrorRepository,
                           TraceLinkRepository traceLinkRepository,
                           TraceLinkGenerator traceLinkGenerator,
                           RevisionNotificationService revisionNotificationService) {
        this.traceLinkService = traceLinkService;
        this.artifactRepository = artifactRepository;
        this.artifactTypeRepository = artifactTypeRepository;
        this.parserErrorRepository = parserErrorRepository;
        this.traceLinkRepository = traceLinkRepository;
        this.traceLinkGenerator = traceLinkGenerator;
        this.revisionNotificationService = revisionNotificationService;
    }

    /**
     * Responsible for parsing a Json objects specifying a trace matrix
     * within of the project's tim.json file. This requires that all referenced
     * artifacts (and their types) have been built.
     *
     * @param projectVersion        the project associated with trace matrix file
     * @param traceMatrixDefinition the JSON object containing the specification
     * @throws ServerError thrown on any parsing error of tim.json or its subsequent files
     */
    public void parseTraceMatrixDefinition(ProjectVersion projectVersion,
                                           JSONObject traceMatrixDefinition) throws ServerError {
        Project project = projectVersion.getProject();
        String fileName = traceMatrixDefinition.getString("file"); // TODO: Make constants and perform validation
        boolean isGenerated = traceMatrixDefinition.has("generatelinks")
            && traceMatrixDefinition.getBoolean("generatelinks");

        Pair<ArtifactType, ArtifactType> matrixArtifactTypes = findMatrixArtifactTypes(project, traceMatrixDefinition);
        List<TraceLink> manualLinks = parseTraceFile(projectVersion, matrixArtifactTypes, fileName);
        this.revisionNotificationService.saveAndBroadcastTraceLinks(project, manualLinks);
        List<TraceLink> generatedLinks = new ArrayList<>();
        if (isGenerated) {
            generatedLinks.addAll(traceLinkGenerator.generateTraceLinksToFile(projectVersion, matrixArtifactTypes));
        }
        this.revisionNotificationService.saveAndBroadcastTraceLinks(project, generatedLinks);
    }

    /**
     * Responsible for finding the source and target type for a trace matrix definition.
     *
     * @param project               the project whose types are being queried.
     * @param traceMatrixDefinition the json defining the source and target types.
     * @return Pair containing source and target types respectively
     * @throws ServerError throws error when either source or target types are not found
     */
    public Pair<ArtifactType, ArtifactType> findMatrixArtifactTypes(Project project,
                                                                    JSONObject traceMatrixDefinition)
        throws ServerError {
        String sourceTypeName = traceMatrixDefinition.getString(SOURCE_PARAM);
        String targetTypeName = traceMatrixDefinition.getString(TARGET_PARAM);
        Optional<ArtifactType> sourceTypeQuery = this.artifactTypeRepository
            .findByProjectAndNameIgnoreCase(project, sourceTypeName);

        if (!sourceTypeQuery.isPresent()) {
            String errorMessage = "Source artifact type does not exist: %s";
            String error = String.format(errorMessage, sourceTypeName);
            throw new ServerError(error);
        }

        Optional<ArtifactType> targetTypeQuery = this.artifactTypeRepository
            .findByProjectAndNameIgnoreCase(project, targetTypeName);
        if (!targetTypeQuery.isPresent()) {
            String errorMessage = "Target artifact type does not exist: %s";
            String error = String.format(errorMessage, targetTypeName);
            throw new ServerError(error);
        }

        return Pair.with(sourceTypeQuery.get(), targetTypeQuery.get());
    }

    public List<TraceLink> parseTraceFile(ProjectVersion projectVersion,
                                          Pair<ArtifactType, ArtifactType> matrixArtifactTypes,
                                          String fileName) throws ServerError {
        Project project = projectVersion.getProject();
        String pathToFile = ProjectPaths.getPathToFlatFile(project, fileName);
        CSVParser traceFileParser = FileUtilities.readCSVFile(pathToFile);
        FileUtilities.assertHasColumns(traceFileParser, REQUIRED_COLUMNS);
        List<CSVRecord> records;
        try {
            records = traceFileParser.getRecords();
        } catch (IOException e) {
            throw new ServerError("unable to read trace file: " + fileName, e);
        }

        List<TraceLink> traceLinks = new ArrayList<>();

        for (CSVRecord record : records) {
            String sourceId = record.get(SOURCE_PARAM).trim();
            String targetId = record.get(TARGET_PARAM).trim();
            Pair<TraceLink, ParserError> traceResult = traceLinkService.createTrace(projectVersion, sourceId,
                targetId);
            if (traceResult.getValue0() != null) {
                traceLinks.add(traceResult.getValue0());
            } else {
                traceResult.getValue1().setFileSource(fileName, traceFileParser.getCurrentLineNumber());
                this.parserErrorRepository.save(traceResult.getValue1());
            }
        }
        return traceLinks;
    }
}
