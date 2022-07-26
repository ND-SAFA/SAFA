package edu.nd.crc.safa.builders;

import java.io.File;
import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.utilities.FileUtilities;

import org.json.JSONArray;
import org.json.JSONObject;

/**
 * Defines series of types that HTTP responses can be parsed into.
 */
public interface ResponseParser {
    /**
     * Parses HTTP request response content into a JSON object.
     *
     * @param content HTTP request response.
     * @return JSONObject
     */
    static JSONObject jsonCreator(String content) {
        return content.length() == 0 ? new JSONObject() : new JSONObject(content);
    }

    /**
     * Parses HTTP request response content into a JSON object.
     *
     * @param content HTTP request response.
     * @return JSONArray
     */
    static JSONArray arrayCreator(String content) {
        return content.length() == 0 ? new JSONArray() : new JSONArray(content);
    }

    /**
     * Parses HTTP request response content into a JSON object.
     *
     * @param content HTTP request response.
     * @return List of files contained in zip file sent through response.
     */
    static List<File> zipFileParser(String content) {
        try {
            return FileUtilities.extractFilesFromZipContent(content);
        } catch (IOException e) {
            e.printStackTrace();
            throw new RuntimeException(e);
        }
    }
}
