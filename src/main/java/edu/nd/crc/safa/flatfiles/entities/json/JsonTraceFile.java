package edu.nd.crc.safa.flatfiles.entities.json;

import java.io.File;
import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.flatfiles.entities.AbstractTraceFile;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;
import edu.nd.crc.safa.utilities.FileUtilities;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.javatuples.Pair;
import org.json.JSONArray;
import org.json.JSONObject;
import org.springframework.web.multipart.MultipartFile;

/**
 * JSON file defining a set of trace links.
 */
public class JsonTraceFile extends AbstractTraceFile<JSONObject> {
    public JsonTraceFile(String pathToFile) throws IOException {
        super(pathToFile);
        throw new SafaError("JSON Not implemented yet");
    }

    public JsonTraceFile(MultipartFile file) throws IOException {
        super(file);
    }

    @Override
    protected void exportAsFileContent(File file) throws IOException {
        JSONObject fileContent = new JSONObject();
        JSONArray jsonArray = new JSONArray();
        ObjectMapper objectMapper = new ObjectMapper();

        for (TraceAppEntity traceAppEntity : this.entities) {
            String objectString = objectMapper.writeValueAsString(traceAppEntity);
            JSONObject jsonObject = new JSONObject(objectString);
            jsonArray.put(jsonObject);
        }
        fileContent.put(Constants.JSON_TRACE_KEY, jsonArray);
        FileUtilities.writeToFile(file, fileContent.toString());
    }

    @Override
    public List<JSONObject> readFileRecords(String pathToFile) throws IOException {
        JSONObject fileContent = FileUtilities.readJSONFile(pathToFile);
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
            ObjectMapper mapper = new ObjectMapper();
            TraceAppEntity artifactAppEntity = mapper.readValue(entityRecord.toString(), TraceAppEntity.class);
            return new Pair<>(artifactAppEntity, null);
        } catch (Exception e) {
            return new Pair<>(null, e.getMessage());
        }
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Constants {
        public static final String JSON_TRACE_KEY = "traces";
    }
}
