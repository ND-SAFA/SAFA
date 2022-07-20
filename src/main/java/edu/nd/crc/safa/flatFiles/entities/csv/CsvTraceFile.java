package edu.nd.crc.safa.flatFiles.entities.csv;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.flatFiles.entities.AbstractDataFile;
import edu.nd.crc.safa.flatFiles.entities.AbstractTraceFile;
import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;

import org.apache.commons.csv.CSVRecord;
import org.javatuples.Pair;
import org.springframework.web.multipart.MultipartFile;

/**
 * Reads trace links from a CSV file.
 */
public class CsvTraceFile extends AbstractDataFile<TraceAppEntity, CSVRecord> {
    public CsvTraceFile(String pathToFile) throws IOException {
        super(pathToFile);
    }

    public CsvTraceFile(MultipartFile file) throws IOException {
        super(file);
    }

    @Override
    public List<String> validate(List<TraceAppEntity> entities, ProjectCommit projectCommit) {
        return new ArrayList<>();
    }

    @Override
    public List<CSVRecord> readFileRecords(String pathToFile) throws IOException {
        return CsvReader.readTraceFile(pathToFile);
    }

    @Override
    public List<CSVRecord> readFileRecords(MultipartFile file) throws IOException {
        return CsvReader.readTraceFile(file);
    }

    @Override
    public Pair<TraceAppEntity, String> parseRecord(CSVRecord entityRecord) {
        String sourceName = entityRecord.get(AbstractTraceFile.Constants.SOURCE_PARAM).trim();
        String targetName = entityRecord.get(AbstractTraceFile.Constants.TARGET_PARAM).trim();
        TraceAppEntity traceAppEntity = new TraceAppEntity()
            .asManualTrace()
            .betweenArtifacts(sourceName, targetName);
        return new Pair<>(traceAppEntity, null);
    }
}
