package edu.nd.crc.safa.flatFiles.entities.json;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.server.entities.api.SafaError;

import org.json.JSONArray;
import org.json.JSONObject;

/**
 * Responsible for reading json files
 * TODO: Copy CSV reader methods and create interface
 */
public class JsonReader {
    public static List<JSONObject> parseFileContent(JSONObject fileContent, String arrayKey) {
        if (!fileContent.has(arrayKey)) {
            throw new SafaError("Expected file to contain key: " + arrayKey);
        }
        JSONArray jsonArtifactArray = fileContent.getJSONArray(arrayKey);
        List<JSONObject> jsonArtifacts = new ArrayList<>();

        for (int i = 0; i < jsonArtifactArray.length(); i++) {
            jsonArtifacts.add(jsonArtifactArray.getJSONObject(i));
        }

        return jsonArtifacts;
    }
}
