package edu.nd.crc.safa.importer.flatfile;

import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.database.entities.Artifact;
import edu.nd.crc.safa.database.entities.ArtifactType;
import edu.nd.crc.safa.database.entities.ParserError;
import edu.nd.crc.safa.database.entities.Project;
import edu.nd.crc.safa.database.entities.ProjectVersion;
import edu.nd.crc.safa.database.entities.TraceLink;
import edu.nd.crc.safa.database.entities.TraceMatrix;
import edu.nd.crc.safa.database.repositories.ArtifactRepository;
import edu.nd.crc.safa.database.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.database.repositories.ParserErrorRepository;
import edu.nd.crc.safa.database.repositories.TraceLinkRepository;
import edu.nd.crc.safa.database.repositories.TraceMatrixRepository;
import edu.nd.crc.safa.error.ServerError;

import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/**
 * Responsible for parsing, validating, and creating trace links.
 */
@Component
public class TraceFileParser {

    private final String SOURCE_PARAM = "source";
    private final String TARGET_PARAM = "target";
    private final String FILE_PARAM = "file";
    private final String[] REQUIRED_COLUMNS = new String[]{SOURCE_PARAM, TARGET_PARAM, FILE_PARAM};

    ArtifactRepository artifactRepository;
    ArtifactTypeRepository artifactTypeRepository;
    TraceMatrixRepository traceMatrixRepository;
    ParserErrorRepository parserErrorRepository;
    TraceLinkRepository traceLinkRepository;
    Generator traceLinkGenerator;

    @Autowired
    public TraceFileParser(ArtifactRepository artifactRepository,
                           ArtifactTypeRepository artifactTypeRepository,
                           TraceMatrixRepository traceMatrixRepository,
                           ParserErrorRepository parserErrorRepository,
                           TraceLinkRepository traceLinkRepository,
                           Generator traceLinkGenerator) {
        this.artifactRepository = artifactRepository;
        this.artifactTypeRepository = artifactTypeRepository;
        this.traceMatrixRepository = traceMatrixRepository;
        this.parserErrorRepository = parserErrorRepository;
        this.traceLinkRepository = traceLinkRepository;
        this.traceLinkGenerator = traceLinkGenerator;
    }


    /**
     * Responsible for parsing a Json objects specifying a trace matrix
     * within of the project's tim.json file. This requires that all referenced
     * artifacts (and their types) have been built.
     *
     * @param project the project associated with trace matrix file
     * @param timJson the JSON object containing the specification
     * @throws ServerError thrown on any parsing error of tim.json or its subsequent files
     */
    public void parseTraceMatrixJson(Project project,
                                     ProjectVersion projectVersion,
                                     JSONObject timJson) throws ServerError {

        String sourceTypeName = timJson.getString(SOURCE_PARAM);
        String targetTypeName = timJson.getString(TARGET_PARAM);
        String fileName = timJson.getString("file");
        boolean isGenerated = timJson.has("generateLinks") && timJson.getBoolean("generateLinks");

        ArtifactType sourceType = this.artifactTypeRepository.findByProjectAndName(project, sourceTypeName);
        ArtifactType targetType = this.artifactTypeRepository.findByProjectAndName(project, targetTypeName);

        if (sourceType == null || targetType == null) {
            String errorMessage = "Could not find source artifacts [%s] for %s";
            String failingType = sourceType == null ? sourceTypeName : targetTypeName;
            String error = String.format(errorMessage, failingType, fileName);
            throw new ServerError(error);
        }

        TraceMatrix traceMatrix = new TraceMatrix(project,
            sourceType,
            targetType,
            isGenerated);
        this.traceMatrixRepository.save(traceMatrix);

        if (!isGenerated) {
            parseTraceFile(project, sourceType, targetType, fileName);
        } else { // TODO: trace link generation
            traceLinkGenerator.generateTraceLink(project, projectVersion, sourceType, targetType, fileName);
            parseTraceFile(project, sourceType, targetType, fileName);
        }
    }

    public void parseTraceFile(Project project,
                               ArtifactType sourceType,
                               ArtifactType targetType,
                               String fileName) throws ServerError {
        CSVParser traceFileParser = FileUtilities.readCSVFile(project, fileName);
        if (!FileUtilities.hasColumns(traceFileParser, REQUIRED_COLUMNS)) {
            String error = "Trace file (%s) is missing at least one required columns (%s)";
            throw new ServerError(String.format(error, fileName, FileUtilities.toString(REQUIRED_COLUMNS)));
        }
        List<CSVRecord> records;
        try {
            records = traceFileParser.getRecords();
        } catch (IOException e) {
            throw new ServerError("unable to read trace file: " + fileName, e);
        }

        for (CSVRecord record : records) {
            try {
                String sourceId = record.get(SOURCE_PARAM).trim();
                String targetId = record.get(TARGET_PARAM).trim();

                Artifact sourceArtifact = this.artifactRepository.findByProjectAndArtifactTypeAndName(project,
                    sourceType,
                    sourceId);
                Artifact targetArtifact = this.artifactRepository.findByProjectAndArtifactTypeAndName(project,
                    targetType,
                    targetId);
                if (sourceArtifact == null) {
                    throw new ServerError("unable to find source artifact: " + sourceId);
                } else if (targetArtifact == null) {
                    throw new ServerError("unable to find target artifact: " + sourceId);
                }

                TraceLink traceLink = new TraceLink(sourceArtifact, targetArtifact);
                traceLink.setIsManual();
                this.traceLinkRepository.save(traceLink);
            } catch (ServerError e) {
                ParserError parserError = new ParserError(project, fileName, traceFileParser.getCurrentLineNumber(),
                    e.getMessage());
                this.parserErrorRepository.save(parserError);
            }
        }
    }
}
