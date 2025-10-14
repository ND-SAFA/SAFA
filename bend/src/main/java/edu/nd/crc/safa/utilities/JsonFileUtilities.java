package edu.nd.crc.safa.utilities;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.config.ObjectMapperConfig;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.commons.io.FileUtils;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

/**
 * Extracts list of records in JSON files containing entities to be extracted as records.
 */
public interface JsonFileUtilities {
    /**
     * Returns the JSONObject parsed from path to JSON file.
     *
     * @param path The path to the JSON file.
     * @return JSONObject
     * @throws IOException If file is missing or not able to be read.
     */
    static JSONObject readJSONFile(String path) throws IOException {
        String fileContent = FileUtils.readFileToString(new File(path), StandardCharsets.UTF_8);
        return new JSONObject(fileContent);
    }

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
            throw new SafaError("Expected file to contain key: %s.", arrayKeyName);
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
        ObjectMapper objectMapper = ObjectMapperConfig.create();
        for (Object entity : entities) {
            String entityContent = objectMapper.writeValueAsString(entity);
            jsonArray.put(new JSONObject(entityContent));
        }
        jsonObject.put(paramName, jsonArray);
        return jsonObject;
    }

    /**
     * Converts object to JSONObject using Jackson ObjectMapper.
     *
     * @param object The object to convert to JSON
     * @return JSON representation of object
     */
    static JSONObject toJson(Object object) {
        ObjectMapper objectMapper = ObjectMapperConfig.create();
        objectMapper.findAndRegisterModules();
        return wrapReturnValue(() -> {
            String objectJsonString = objectMapper.writeValueAsString(object);
            return new JSONObject(objectJsonString);
        });
    }

    static JSONArray toJsonArray(Object object) {
        ObjectMapper objectMapper = ObjectMapperConfig.create();
        return wrapReturnValue(() -> {
            String objectJsonString = objectMapper.writeValueAsString(object);
            return new JSONArray(objectJsonString);
        });
    }

    /**
     * Converts JSON string to instance of java class.
     *
     * @param jsonString  Object json as string.
     * @param exportClass Class to convert object to
     * @param <T>         The type that gets parsed
     * @return Instance of specified class.
     */
    static <T> T parse(String jsonString, Class<T> exportClass) {
        ObjectMapper objectMapper = ObjectMapperConfig.create();
        JSONObject jsonObject = new JSONObject(jsonString);
        return wrapReturnValue(() -> objectMapper.readValue(jsonObject.toString(), exportClass));
    }

    /**
     * Converts JSON string to instance of java class.
     *
     * @param jsonString  Object json as string.
     * @param exportClass Class to convert object to
     * @param <T>         The type that gets parsed
     * @return Instance of specified class.
     */
    static <T> T parse(String jsonString, TypeReference<T> exportClass) {
        ObjectMapper objectMapper = ObjectMapperConfig.create();
        JSONObject jsonObject = jsonString.isEmpty() ? new JSONObject() : new JSONObject(jsonString);
        return wrapReturnValue(() -> objectMapper.readValue(jsonObject.toString(), exportClass));
    }

    /**
     * Attempts to parse json string and returns result.
     *
     * @param json The string to parse.
     * @return True if valid JSON, false otherwise.
     */
    static boolean isValid(String json) {
        try {
            new JSONObject(json);
        } catch (JSONException e) {
            return false;
        }
        return true;
    }

    private static <T> T wrapReturnValue(ThrowingSupplier<T> supplier) {
        try {
            return supplier.get();
        } catch (Exception e) {
            throw new SafaError(e.getMessage());
        }
    }

    @FunctionalInterface
    interface ThrowingSupplier<T> {
        T get() throws JsonProcessingException;
    }
}
