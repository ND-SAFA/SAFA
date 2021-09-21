package edu.nd.crc.safa.importer.flatfiles;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.db.entities.sql.ApplicationActivity;
import edu.nd.crc.safa.server.db.entities.sql.Artifact;
import edu.nd.crc.safa.server.db.entities.sql.ArtifactType;
import edu.nd.crc.safa.server.db.entities.sql.ParserError;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.db.entities.sql.TraceLink;
import edu.nd.crc.safa.server.db.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.db.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.server.db.repositories.ParserErrorRepository;
import edu.nd.crc.safa.server.db.repositories.TraceLinkRepository;
import edu.nd.crc.safa.server.responses.ServerError;
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

    ArtifactRepository artifactRepository;
    ArtifactTypeRepository artifactTypeRepository;
    ParserErrorRepository parserErrorRepository;
    TraceLinkRepository traceLinkRepository;
    TraceLinkGenerator traceLinkGenerator;

    @Autowired
    public TraceFileParser(ArtifactRepository artifactRepository,
                           ArtifactTypeRepository artifactTypeRepository,
                           ParserErrorRepository parserErrorRepository,
                           TraceLinkRepository traceLinkRepository,
                           TraceLinkGenerator traceLinkGenerator) {
        this.artifactRepository = artifactRepository;
        this.artifactTypeRepository = artifactTypeRepository;
        this.parserErrorRepository = parserErrorRepository;
        this.traceLinkRepository = traceLinkRepository;
        this.traceLinkGenerator = traceLinkGenerator;
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
        parseTraceFile(projectVersion, matrixArtifactTypes, fileName);

        if (isGenerated) {
            traceLinkGenerator.generateTraceLinksToFile(projectVersion, matrixArtifactTypes);
        }
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

    public void parseTraceFile(ProjectVersion projectVersion,
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

        try {
            for (CSVRecord record : records) {
                String sourceId = record.get(SOURCE_PARAM).trim();
                String targetId = record.get(TARGET_PARAM).trim();
                Pair<String, String> artifactIds = new Pair<>(sourceId, targetId);
                TraceLink newLink = createTraceLink(project, matrixArtifactTypes, artifactIds);
                traceLinks.add(newLink);
            }
            System.out.println("Saving # links" + traceLinks.size());
            this.traceLinkRepository.saveAll(traceLinks);
        } catch (ServerError e) {
            ParserError parserError = new ParserError(projectVersion,
                e.getMessage(),
                ApplicationActivity.PARSING_TRACES,
                fileName,
                traceFileParser.getCurrentLineNumber());
            this.parserErrorRepository.save(parserError);
        }
    }

    /**
     * Creates a trace links between the artifacts corresponding with source type + id and
     * target source + id within given project.
     *
     * @param project       The project with associated artifact types and artifacts.
     * @param artifactTypes The source and target types of artifact associated with trace links.
     * @param artifactNames The source and target names of artifact associated with trace links.
     * @return unsaved TraceLink containing source and target artifacts identifed by the above params.
     * @throws ServerError If either source or target artifact are not found.
     */
    public TraceLink createTraceLink(Project project,
                                     Pair<ArtifactType, ArtifactType> artifactTypes,
                                     Pair<String, String> artifactNames) throws ServerError {
        ArtifactType sourceType = artifactTypes.getValue0();
        String sourceId = artifactNames.getValue0();
        Optional<Artifact> sourceArtifactQuery = this.artifactRepository
            .findByProjectAndTypeAndNameIgnoreCase(project, sourceType, sourceId);
        if (!sourceArtifactQuery.isPresent()) {
            throw new ServerError("Source artifact does not exist: " + sourceId);
        }
        Artifact sourceArtifact = sourceArtifactQuery.get();

        ArtifactType targetType = artifactTypes.getValue1();
        String targetId = artifactNames.getValue1();
        Optional<Artifact> targetArtifactQuery = this.artifactRepository
            .findByProjectAndTypeAndNameIgnoreCase(project, targetType, targetId);
        if (!targetArtifactQuery.isPresent()) {
            throw new ServerError("Target artifact does not exist: " + sourceId);
        }
        Artifact targetArtifact = targetArtifactQuery.get();

        return this.traceLinkRepository
            .getApprovedLinkIfExist(sourceArtifact, targetArtifact)
            .orElseGet(() -> new TraceLink(sourceArtifact, targetArtifact));
    }
}
