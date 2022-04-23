package edu.nd.crc.safa.importer.flatfiles;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.api.TraceGenerationRequest;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.artifacts.ArtifactTypeRepository;
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

    @Autowired
    public TraceFileParser(ArtifactTypeRepository artifactTypeRepository) {
        this.artifactTypeRepository = artifactTypeRepository;
    }

    public Pair<List<TraceAppEntity>, List<TraceGenerationRequest>> parseTraceFiles(ProjectVersion projectVersion,
                                                                                    JSONObject timFileJson) throws SafaError {
        List<TraceAppEntity> traces = new ArrayList<>();
        List<TraceGenerationRequest> traceGenerationRequests = new ArrayList<>();

        for (Iterator<String> keyIterator = timFileJson.keys(); keyIterator.hasNext(); ) {
            String traceMatrixKey = keyIterator.next();
            if (traceMatrixKey.equalsIgnoreCase(ProjectVariables.DATAFILES_PARAM)) {
                continue;
            }
            JSONObject traceMatrix = timFileJson.getJSONObject(traceMatrixKey);
            String fileName = traceMatrix.getString("file"); // TODO: Make constants and perform validation
            traces.addAll(readAndParseTraceFile(projectVersion, fileName));

            boolean isGenerated = traceMatrix.has("generatelinks")
                && traceMatrix.getBoolean("generatelinks");
            if (isGenerated) {
                String source = traceMatrix.getString(SOURCE_PARAM);
                String target = traceMatrix.getString(TARGET_PARAM);
                TraceGenerationRequest traceGenerationRequest = new TraceGenerationRequest(source, target);
                traceGenerationRequests.add(traceGenerationRequest);
            }
        }
        return new Pair<>(traces, traceGenerationRequests);
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
            traceLinks.add(new TraceAppEntity()
                .asManualTrace()
                .betweenArtifacts(sourceName, targetName));
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

    public ArtifactType findArtifactTypeFromTraceMatrixDefinition(Project project, String typeName)
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
