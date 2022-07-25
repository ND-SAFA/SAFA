package edu.nd.crc.safa.flatfiles.entities.json;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.server.entities.api.SafaError;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.json.JSONArray;
import org.json.JSONObject;

/**
 * Extracts list of records in JSON files containing entities to be extracted as records.
 */
public interface JsonFileUtilities {
    /**
     * Reads JSON file and extracts array using given key and converts them to a list of
     * json objects.
     *
     * @param jsonFile     The file containing the array.
     * @param arrayKeyName The key the array is under in given json object.
     * @return List of objects representing given array.
     */
    static List<JSONObject> getArrayAsRecords(JSONObject jsonFile, String arrayKeyName) {
        if (!jsonFile.has(arrayKeyName)) {
            throw new SafaError("Expected file to contain key: " + arrayKeyName);
        }
        JSONArray jsonArtifactArray = jsonFile.getJSONArray(arrayKeyName);
        List<JSONObject> jsonArtifacts = new ArrayList<>();

        for (int i = 0; i < jsonArtifactArray.length(); i++) {
            jsonArtifacts.add(jsonArtifactArray.getJSONObject(i));
        }

        return jsonArtifacts;
    }

    /**
     * Converts given entities to a JSON object containing array of entities under param name.
     *
     * @param entities  The entities to parse and store in the JSON object.
     * @param paramName The name containing the entities in the JSON object.
     * @return JSONObject containing parsed entities.
     * @throws JsonProcessingException Throws error if entity cannot be parsed into JSON
     */
    static JSONObject writeEntitiesAsJson(List<? extends Object> entities,
                                          String paramName) throws JsonProcessingException {
        JSONObject jsonObject = new JSONObject();
        JSONArray jsonArray = new JSONArray();
        ObjectMapper objectMapper = new ObjectMapper();
        for (Object entity : entities) {
            String entityContent = objectMapper.writeValueAsString(entity);
            jsonArray.put(new JSONObject(entityContent));
        }
        jsonObject.put(paramName, jsonArray);
        return jsonObject;
    }
}
