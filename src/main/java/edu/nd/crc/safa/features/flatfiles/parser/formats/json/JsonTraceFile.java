package edu.nd.crc.safa.features.flatfiles.parser.formats.json;

import java.io.File;
import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.config.ObjectMapperConfig;
import edu.nd.crc.safa.features.flatfiles.parser.base.AbstractTraceFile;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.utilities.FileUtilities;
import edu.nd.crc.safa.utilities.JsonFileUtilities;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.javatuples.Pair;
import org.json.JSONObject;
import org.springframework.web.multipart.MultipartFile;

/**
 * JSON file defining a set of trace links.
 */
public class JsonTraceFile extends AbstractTraceFile<JSONObject> {

    public JsonTraceFile(List<TraceAppEntity> traces) {
        super(traces);
    }

    public JsonTraceFile(String pathToFile) throws IOException {
        super(pathToFile);
    }

    public JsonTraceFile(MultipartFile file) throws IOException {
        super(file);
    }

    @Override
    protected void exportAsFileContent(File file) throws IOException {
        JSONObject fileContent = JsonFileUtilities.writeEntitiesAsJson(this.getEntities(),
            Constants.JSON_TRACE_KEY);
        FileUtilities.writeToFile(file, fileContent.toString());
    }

    @Override
    public List<JSONObject> readFileRecords(String pathToFile) throws IOException {
        JSONObject fileContent = JsonFileUtilities.readJSONFile(pathToFile);
        return JsonFileUtilities.getArrayAsRecords(fileContent, Constants.JSON_TRACE_KEY);
    }

    @Override
    public List<JSONObject> readFileRecords(MultipartFile file) throws IOException {
        JSONObject fileContent = FileUtilities.readMultiPartJSONFile(file);
        return JsonFileUtilities.getArrayAsRecords(fileContent, Constants.JSON_TRACE_KEY);
    }

    @Override
    public Pair<TraceAppEntity, String> parseRecord(JSONObject entityRecord) {
        try {
            //TODO : make this the default logic for parsing json records with specified generic class
            ObjectMapper mapper = ObjectMapperConfig.create();
            TraceAppEntity traceAppEntity = mapper.readValue(entityRecord.toString(), TraceAppEntity.class);

            List<String> missingFields = traceAppEntity.getMissingRequiredFields();
            if (missingFields.size() == 0) {
                return new Pair<>(traceAppEntity, null);
            } else {
                return new Pair<>(null,
                    String.format("Trace missing one or more required fields: %s", missingFields));
            }
        } catch (Exception e) {
            return new Pair<>(null, e.getMessage());
        }
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Constants {
        public static final String JSON_TRACE_KEY = "traces";
    }
}
