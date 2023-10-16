package edu.nd.crc.safa.features.flatfiles.parser.formats.csv;

import java.io.File;
import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.features.flatfiles.parser.base.AbstractTraceFile;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.utilities.CsvFileUtilities;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.apache.commons.csv.CSVRecord;
import org.javatuples.Pair;
import org.springframework.web.multipart.MultipartFile;

/**
 * Reads trace links from a CSV file.
 */
public class CsvTraceFile extends AbstractTraceFile<CSVRecord> {

    public CsvTraceFile(List<TraceAppEntity> traces) {
        super(traces);
    }

    public CsvTraceFile(String pathToFile) throws IOException {
        super(pathToFile);
    }

    public CsvTraceFile(MultipartFile file) throws IOException {
        super(file);
    }

    @Override
    protected void exportAsFileContent(File file) throws IOException {
        CsvFileUtilities.writeEntitiesAsCsvFile(file,
            Constants.ALL_COLUMNS,
            this.getEntities(),
            this::getTraceRow);
    }

    private String[] getTraceRow(TraceAppEntity traceAppEntity) {
        return new String[]{
            traceAppEntity.getSourceName(),
            traceAppEntity.getTargetName(),
            traceAppEntity.getExplanation()
        };
    }

    @Override
    public List<CSVRecord> readFileRecords(String pathToFile) throws IOException {
        return CsvFileUtilities.readTraceFile(pathToFile);
    }

    @Override
    public List<CSVRecord> readFileRecords(MultipartFile file) throws IOException {
        return CsvFileUtilities.readTraceFile(file);
    }

    @Override
    public Pair<TraceAppEntity, String> parseRecord(CSVRecord entityRecord) {
        String sourceName = entityRecord.get(Constants.SOURCE_PARAM).trim();
        String targetName = entityRecord.get(Constants.TARGET_PARAM).trim();
        TraceAppEntity traceAppEntity = new TraceAppEntity()
            .asManualTrace()
            .betweenArtifacts(sourceName, targetName);

        if (entityRecord.isSet(Constants.EXPLANATION_PARAM)) {
            traceAppEntity.setExplanation(entityRecord.get(Constants.EXPLANATION_PARAM));
        }

        return new Pair<>(traceAppEntity, null);
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Constants {
        public static final String SOURCE_PARAM = "source";
        public static final String TARGET_PARAM = "target";
        public static final String EXPLANATION_PARAM = "explanation";
        public static final String[] REQUIRED_COLUMNS = new String[]{SOURCE_PARAM, TARGET_PARAM};
        public static final String[] ALL_COLUMNS = new String[]{SOURCE_PARAM, TARGET_PARAM, EXPLANATION_PARAM};
    }
}
