package edu.nd.crc.safa.importer.flatfiles;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.importer.tracegenerator.TraceLinkGenerator;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.utilities.FileUtilities;

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

    private final ArtifactTypeRepository artifactTypeRepository;
    private final TraceLinkGenerator traceLinkGenerator;

    @Autowired
    public TraceFileParser(ArtifactTypeRepository artifactTypeRepository,
                           TraceLinkGenerator traceLinkGenerator) {
        this.artifactTypeRepository = artifactTypeRepository;
        this.traceLinkGenerator = traceLinkGenerator;
    }

    public List<TraceAppEntity> parseTraceFiles(ProjectVersion projectVersion,
                                                JSONObject timFileJson) throws SafaError {
        List<TraceAppEntity> traces = new ArrayList<>();
        for (Iterator<String> keyIterator = timFileJson.keys(); keyIterator.hasNext(); ) {
            String traceMatrixKey = keyIterator.next();
            if (traceMatrixKey.equalsIgnoreCase(ProjectVariables.DATAFILES_PARAM)) {
                continue;
            }
            traces.addAll(this.parseTraceMatrixDefinition(projectVersion,
                timFileJson.getJSONObject(traceMatrixKey)));
        }
        return traces;
    }

    /**
     * Responsible for parsing a Json objects specifying a trace matrix
     * within of the project's tim.json file. Note, this function performs no validation
     * is purely a translation from file to json.
     *
     * @param projectVersion        the project associated with trace matrix file
     * @param traceMatrixDefinition the JSON object containing the specification
     * @throws SafaError thrown on any parsing error of tim.json or its subsequent files
     */
    private List<TraceAppEntity> parseTraceMatrixDefinition(ProjectVersion projectVersion,
                                                            JSONObject traceMatrixDefinition) throws SafaError {
        Project project = projectVersion.getProject();
        String fileName = traceMatrixDefinition.getString("file"); // TODO: Make constants and perform validation
        boolean isGenerated = traceMatrixDefinition.has("generatelinks")
            && traceMatrixDefinition.getBoolean("generatelinks");

        Pair<ArtifactType, ArtifactType> matrixArtifactTypes = findMatrixArtifactTypes(project, traceMatrixDefinition);

        List<TraceAppEntity> projectLinks = new ArrayList<>();

        if (isGenerated) {
            List<TraceAppEntity> generatedLinks = traceLinkGenerator
                .generateTraceLinksToFile(projectVersion, matrixArtifactTypes);
            projectLinks.addAll(generatedLinks);
        }
        projectLinks.addAll(readAndParseTraceFile(projectVersion, fileName));
        return projectLinks;
    }

    /**
     * Responsible for finding the source and target type for a trace matrix definition.
     *
     * @param project               The project whose types are being queried.
     * @param traceMatrixDefinition The json defining the source and target types.
     * @return Pair containing source and target types respectively
     * @throws SafaError throws error when either source or target types are not found
     */
    public Pair<ArtifactType, ArtifactType> findMatrixArtifactTypes(Project project,
                                                                    JSONObject traceMatrixDefinition)
        throws SafaError {
        String sourceTypeName = traceMatrixDefinition.getString(SOURCE_PARAM);
        String targetTypeName = traceMatrixDefinition.getString(TARGET_PARAM);
        ArtifactType sourceType = findArtifactTypeFromTraceMatrixDefinition(project, sourceTypeName);
        ArtifactType targetType = findArtifactTypeFromTraceMatrixDefinition(project, targetTypeName);
        return Pair.with(sourceType, targetType);
    }

    public List<TraceAppEntity> readAndParseTraceFile(ProjectVersion projectVersion,
                                                      String fileName) throws SafaError {
        Project project = projectVersion.getProject();
        String pathToFile = ProjectPaths.getPathToFlatFile(project, fileName);
        CSVParser traceFileParser = FileUtilities.readCSVFile(pathToFile);

        return parseTraceFile(traceFileParser);
    }

    public List<TraceAppEntity> parseTraceFile(CSVParser traceFileParser)
        throws SafaError {

        List<CSVRecord> records = getRecordsInTraceFile(traceFileParser);
        List<TraceAppEntity> traceLinks = new ArrayList<>();
        for (CSVRecord record : records) {
            String sourceName = record.get(SOURCE_PARAM).trim();
            String targetName = record.get(TARGET_PARAM).trim();
            traceLinks.add(new TraceAppEntity(sourceName, targetName));
        }
        return traceLinks;
    }

    public Pair<List<TraceAppEntity>, List<Pair<String, Long>>> readTraceFile(CSVParser traceFileParser)
        throws SafaError {
        List<CSVRecord> records = getRecordsInTraceFile(traceFileParser);
        List<TraceAppEntity> traceLinks = new ArrayList<>();
        List<Pair<String, Long>> errors = new ArrayList<>();
        for (CSVRecord record : records) {
            String sourceId = record.get(SOURCE_PARAM).trim();
            String targetId = record.get(TARGET_PARAM).trim();
            TraceAppEntity trace = new TraceAppEntity();
            trace.setSourceName(sourceId);
            trace.setTargetName(targetId);
            traceLinks.add(trace);
        }
        return new Pair<>(traceLinks, errors);
    }

    public CSVParser readTraceFile(MultipartFile file) throws SafaError {
        return FileUtilities.readMultiPartCSVFile(file, REQUIRED_COLUMNS);
    }

    private List<CSVRecord> getRecordsInTraceFile(CSVParser fileParser) throws SafaError {
        FileUtilities.assertHasColumns(fileParser, REQUIRED_COLUMNS);
        List<CSVRecord> records;
        try {
            records = fileParser.getRecords();
            return records;
        } catch (IOException e) {
            throw new SafaError("Unable to read trace file.");
        }
    }

    private ArtifactType findArtifactTypeFromTraceMatrixDefinition(Project project, String typeName)
        throws SafaError {
        Optional<ArtifactType> sourceTypeQuery = this.artifactTypeRepository
            .findByProjectAndNameIgnoreCase(project, typeName);

        if (sourceTypeQuery.isEmpty()) {
            List<ArtifactType> artifactTypes = this.artifactTypeRepository.findByProject(project);
            String errorMessage = String.format(
                "Trace matrix definition references unknown type: %s. Defined types include: %s",
                typeName,
                artifactTypes);
            throw new SafaError(errorMessage);
        }
        return sourceTypeQuery.get();
    }
}
