package edu.nd.crc.safa.importer.flatfiles;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.importer.tracegenerator.TraceLinkGenerator;
import edu.nd.crc.safa.server.entities.api.ServerError;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.ApplicationActivity;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.ParserError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceLink;
import edu.nd.crc.safa.server.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.server.repositories.ParserErrorRepository;
import edu.nd.crc.safa.server.repositories.TraceLinkRepository;
import edu.nd.crc.safa.server.services.RevisionNotificationService;
import edu.nd.crc.safa.server.services.TraceLinkService;
import edu.nd.crc.safa.utilities.ArtifactFinder;
import edu.nd.crc.safa.utilities.FileUtilities;
import edu.nd.crc.safa.utilities.TraceLinkFinder;

import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import org.javatuples.Pair;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.multipart.MultipartFile;

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
        List<TraceLink> manualLinks = readAndParseTraceFile(projectVersion, matrixArtifactTypes, fileName);
        this.traceLinkRepository.saveAll(manualLinks);
        List<TraceLink> generatedLinks = new ArrayList<>();
        if (isGenerated) {
            generatedLinks.addAll(traceLinkGenerator.generateTraceLinksToFile(projectVersion, matrixArtifactTypes));
        }
        this.traceLinkRepository.saveAll(generatedLinks);
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
        ArtifactType sourceType = findArtifactType(project, sourceTypeName);
        ArtifactType targetType = findArtifactType(project, targetTypeName);
        return Pair.with(sourceType, targetType);
    }

    public List<TraceLink> readAndParseTraceFile(ProjectVersion projectVersion,
                                                 Pair<ArtifactType, ArtifactType> matrixArtifactTypes,
                                                 String fileName) throws ServerError {
        Project project = projectVersion.getProject();
        String pathToFile = ProjectPaths.getPathToFlatFile(project, fileName);
        CSVParser traceFileParser = FileUtilities.readCSVFile(pathToFile);

        Pair<List<TraceLink>, List<Pair<String, Long>>> parseResponse =
            parseTraceFile((a) -> artifactRepository.findByProjectAndName(project, a),
                (s, t) -> traceLinkService.queryForLinkBetween(s, t),
                traceFileParser);
        List<ParserError> parserErrors = parseResponse.getValue1().stream().map(error -> {
            ParserError parserError = new ParserError(projectVersion, error.getValue0(),
                ApplicationActivity.PARSING_TRACES);
            parserError.setFileSource(fileName, error.getValue1());
            return parserError;
        }).collect(Collectors.toList());
        this.parserErrorRepository.saveAll(parserErrors);
        return parseResponse.getValue0();
    }

    public Pair<List<TraceLink>, List<Pair<String, Long>>> parseTraceFile(ArtifactFinder artifactFinder,
                                                                          TraceLinkFinder traceLinkFinder,
                                                                          CSVParser traceFileParser)
        throws ServerError {
        FileUtilities.assertHasColumns(traceFileParser, REQUIRED_COLUMNS);
        List<CSVRecord> records;
        try {
            records = traceFileParser.getRecords();
        } catch (IOException e) {
            String error = "Unable to read trace file.";
            return new Pair<>(new ArrayList<>(), List.of(new Pair<>(error, (long) -1)));
        }

        List<TraceLink> traceLinks = new ArrayList<>();
        List<Pair<String, Long>> errors = new ArrayList<>();
        for (CSVRecord record : records) {
            String sourceId = record.get(SOURCE_PARAM).trim();
            String targetId = record.get(TARGET_PARAM).trim();
            Pair<TraceLink, String> traceResult = traceLinkService.parseTraceLink(artifactFinder,
                traceLinkFinder,
                sourceId,
                targetId);
            if (traceResult.getValue0() != null) {
                traceLinks.add(traceResult.getValue0());
            }
            if (traceResult.getValue1() != null) {
                errors.add(new Pair<>(traceResult.getValue1(), record.getRecordNumber()));
            }
        }
        return new Pair<>(traceLinks, errors);
    }

    public Pair<List<TraceAppEntity>, List<Pair<String, Long>>> readTraceFile(ArtifactFinder artifactFinder,
                                                                              TraceLinkFinder traceLinkFinder,
                                                                              CSVParser traceFileParser)
        throws ServerError {
        FileUtilities.assertHasColumns(traceFileParser, REQUIRED_COLUMNS);
        List<CSVRecord> records;
        try {
            records = traceFileParser.getRecords();
        } catch (IOException e) {
            String error = "Unable to read trace file.";
            return new Pair<>(new ArrayList<>(), List.of(new Pair<>(error, (long) -1)));
        }

        List<TraceAppEntity> traceLinks = new ArrayList<>();
        List<Pair<String, Long>> errors = new ArrayList<>();
        for (CSVRecord record : records) {
            String sourceId = record.get(SOURCE_PARAM).trim();
            String targetId = record.get(TARGET_PARAM).trim();
            TraceAppEntity trace = new TraceAppEntity();
            trace.setSource(sourceId);
            trace.setTarget(targetId);
            traceLinks.add(trace);
        }
        return new Pair<>(traceLinks, errors);
    }

    public CSVParser readTraceFile(MultipartFile file) throws ServerError {
        return FileUtilities.readMultiPartCSVFile(file, REQUIRED_COLUMNS);
    }

    private ArtifactType findArtifactType(Project project, String typeName) throws ServerError {
        Optional<ArtifactType> sourceTypeQuery = this.artifactTypeRepository
            .findByProjectAndNameIgnoreCase(project, typeName);

        if (sourceTypeQuery.isEmpty()) {
            List<ArtifactType> artifactTypes = this.artifactTypeRepository.findByProject(project);
            String errorMessage = String.format("Unexpected artifact type: %s. Expected one of: %s",
                typeName,
                artifactTypes);
            throw new ServerError(errorMessage);
        }
        return sourceTypeQuery.get();
    }
}
