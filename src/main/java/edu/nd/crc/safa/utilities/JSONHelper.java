package edu.nd.crc.safa.utilities;

import java.util.Hashtable;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import org.json.JSONObject;
import org.springframework.stereotype.Component;

/**
 * Responsible for parsing between Map and JSONObject.
 */
@Component
public class JSONHelper {

    /**
     * Converts given Map into a JSON object.
     *
     * @param map The map to convert.
     * @return JsonObject
     */
    public JSONObject map2Json(Map<String, String> map) {
        List<String> keys = map.keySet()
            .stream()
            .sorted()
            .collect(Collectors.toList());
        JSONObject json = new JSONObject();
        for (String key : keys) {
            json.put(key, map.get(key));
        }
        return json;
    }

    /**
     * Turns given map into json string representation.
     *
     * @param map A map of key-value pairs to stringify.
     * @return JsonObject of the map
     */
    public String stringify(Map<String, String> map) {
        return map2Json(map).toString();
    }

    /**
     * Takes a string as json and converts it into a String map of
     *
     * @param mapJson The json string of the map.
     * @return The converted map.
     */
    public Map<String, String> parse(String mapJson) {
        Hashtable<String, String> hashtable = new Hashtable<>();
        if (mapJson.equals("")) {
            return hashtable;
        }

        JSONObject tableJson = new JSONObject(mapJson);
        for (String key : tableJson.keySet()) {
            hashtable.put(key, tableJson.getString(key));
        }
        return hashtable;
    }
}
