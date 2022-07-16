package edu.nd.crc.safa.builders;

import java.io.File;
import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.utilities.FileUtilities;

import org.json.JSONArray;
import org.json.JSONObject;

public class ResponseParser {
    public static JSONObject jsonCreator(String content) {
        return content.length() == 0 ? new JSONObject() : new JSONObject(content);
    }

    public static JSONArray arrayCreator(String content) {
        return content.length() == 0 ? new JSONArray() : new JSONArray(content);
    }

    public static List<File> zipFileParser(String content) {
        try {
            return FileUtilities.getZipFiles(content);
        } catch (IOException e) {
            e.printStackTrace();
            throw new RuntimeException(e);
        }
    }
}
