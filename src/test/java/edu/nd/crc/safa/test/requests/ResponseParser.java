package edu.nd.crc.safa.test.requests;

import java.io.File;
import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.utilities.FileUtilities;

import org.json.JSONArray;
import org.json.JSONObject;
import org.springframework.util.StringUtils;

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
        return StringUtils.hasLength(content) ? new JSONObject(content) : new JSONObject();
    }

    /**
     * Parses HTTP request response content into a JSON object.
     *
     * @param content HTTP request response.
     * @return JSONArray
     */
    static JSONArray arrayCreator(String content) {
        return StringUtils.hasLength(content) ? new JSONArray(content) : new JSONArray();
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
