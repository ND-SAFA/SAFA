package edu.nd.crc.safa.importer.flatfiles;

import static edu.nd.crc.safa.importer.flatfiles.TIMParser.FILE_PARAM;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.common.EntityCreation;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.utilities.FileUtilities;

import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import org.javatuples.Pair;
import org.json.JSONObject;
import org.springframework.web.multipart.MultipartFile;

/**
 * Responsible for parsing trace files.
 */
public class TraceFileParser {
    public static final String GENERATE_LINKS_PARAM = "generatelinks";
    public static final String SOURCE_PARAM = "source";
    public static final String TARGET_PARAM = "target";
    public static String[] TIM_REQUIRED_KEYS = {SOURCE_PARAM, TARGET_PARAM, FILE_PARAM};
    public static String[] FILE_REQUIRED_COLUMNS = {SOURCE_PARAM, TARGET_PARAM};

    String name;
    String source;
    String target;
    String file;
    boolean isGenerated;

    public TraceFileParser(String name, String source, String target, String file, boolean isGenerated) {
        this.name = name;
        this.source = source;
        this.target = target;
        this.file = file;
        this.isGenerated = isGenerated;
    }

    public static List<CSVRecord> getRecordsInTraceFile(CSVParser fileParser) throws SafaError {
        FileUtilities.assertHasColumns(fileParser, FILE_REQUIRED_COLUMNS);
        List<CSVRecord> records;
        try {
            records = fileParser.getRecords();
            return records;
        } catch (IOException e) {
            throw new SafaError("Unable to read trace file.");
        }
    }

    public static EntityCreation<TraceAppEntity, Pair<String, Long>> readTraceFile(
        MultipartFile file) throws SafaError {
        CSVParser traceFileParser = FileUtilities.readMultiPartCSVFile(file, TraceFileParser.FILE_REQUIRED_COLUMNS);
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
        return new EntityCreation<>(traceLinks, errors);
    }

    public static TraceFileParser fromJson(JSONObject traceMatrix,
                                           String traceMatrixKey,
                                           List<String> artifactTypes) throws SafaError {
        FileUtilities.assertHasKeys(traceMatrix, TraceFileParser.TIM_REQUIRED_KEYS);

        String source = traceMatrix.getString(TraceFileParser.SOURCE_PARAM);
        String target = traceMatrix.getString(TraceFileParser.TARGET_PARAM);
        String file = traceMatrix.getString(FILE_PARAM);

        for (String artifactType : List.of(source, target)) {
            if (!artifactTypes.contains(artifactType.toLowerCase())) {
                throw new SafaError(String.format("Unknown artifact type: %s", artifactType));
            }
        }

        boolean isGenerated = traceMatrix.has(GENERATE_LINKS_PARAM) && traceMatrix.getBoolean(GENERATE_LINKS_PARAM);

        return new TraceFileParser(traceMatrixKey,
            source,
            target,
            file,
            isGenerated);
    }

    public List<TraceAppEntity> readAndParseTraceFile(Project project) throws SafaError {
        String pathToFile = ProjectPaths.getPathToFlatFile(project, this.file);
        CSVParser traceFileParser = FileUtilities.readCSVFile(pathToFile);

        return parseTraceFile(traceFileParser);
    }

    public boolean isGenerated() {
        return isGenerated;
    }

    public void setGenerated(boolean generated) {
        isGenerated = generated;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getSource() {
        return source;
    }

    public void setSource(String source) {
        this.source = source;
    }

    public String getTarget() {
        return target;
    }

    public void setTarget(String target) {
        this.target = target;
    }

    public String getFile() {
        return file;
    }

    public void setFile(String file) {
        this.file = file;
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
}
