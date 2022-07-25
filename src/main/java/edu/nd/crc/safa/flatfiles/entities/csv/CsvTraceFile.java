package edu.nd.crc.safa.flatfiles.entities.csv;

import java.io.File;
import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.flatfiles.entities.AbstractTraceFile;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.apache.commons.csv.CSVRecord;
import org.javatuples.Pair;
import org.springframework.web.multipart.MultipartFile;

/**
 * Reads trace links from a CSV file.
 */
public class CsvTraceFile extends AbstractTraceFile<CSVRecord> {
    public CsvTraceFile(String pathToFile) throws IOException {
        super(pathToFile);
    }

    public CsvTraceFile(MultipartFile file) throws IOException {
        super(file);
    }

    @Override
    protected void exportAsFileContent(File file) throws Exception {
        //TODO:
    }

    @Override
    public List<CSVRecord> readFileRecords(String pathToFile) throws IOException {
        return CsvDataFileReader.readTraceFile(pathToFile);
    }

    @Override
    public List<CSVRecord> readFileRecords(MultipartFile file) throws IOException {
        return CsvDataFileReader.readTraceFile(file);
    }

    @Override
    public Pair<TraceAppEntity, String> parseRecord(CSVRecord entityRecord) {
        String sourceName = entityRecord.get(Constants.SOURCE_PARAM).trim();
        String targetName = entityRecord.get(Constants.TARGET_PARAM).trim();
        TraceAppEntity traceAppEntity = new TraceAppEntity()
            .asManualTrace()
            .betweenArtifacts(sourceName, targetName);
        return new Pair<>(traceAppEntity, null);
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Constants {
        public static final String SOURCE_PARAM = "source";
        public static final String TARGET_PARAM = "target";
        public static final String[] REQUIRED_COLUMNS = new String[]{SOURCE_PARAM, TARGET_PARAM};
    }
}
