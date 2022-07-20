package edu.nd.crc.safa.flatFiles.entities.json;

import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.flatFiles.entities.AbstractTraceFile;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;
import edu.nd.crc.safa.utilities.FileUtilities;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.javatuples.Pair;
import org.json.JSONObject;
import org.springframework.web.multipart.MultipartFile;

public class JsonTraceFile extends AbstractTraceFile<JSONObject> {
    public JsonTraceFile(String pathToFile) throws IOException {
        super(pathToFile);
        throw new SafaError("JSON Not implemented yet");
    }

    public JsonTraceFile(MultipartFile file) throws IOException {
        super(file);
    }

    @Override
    public List<JSONObject> readFileRecords(String pathToFile) throws IOException {
        JSONObject fileContent = FileUtilities.readJSONFile(pathToFile);
        return JsonReader.parseFileContent(fileContent, JsonTraceFile.JsonTraceConstants.JSON_TRACE_KEY);
    }

    @Override
    public List<JSONObject> readFileRecords(MultipartFile file) throws IOException {
        JSONObject fileContent = FileUtilities.readMultiPartJSONFile(file);
        return JsonReader.parseFileContent(fileContent, JsonTraceFile.JsonTraceConstants.JSON_TRACE_KEY);
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

    public static class JsonTraceConstants {
        public static final String JSON_TRACE_KEY = "traces";
    }
}
