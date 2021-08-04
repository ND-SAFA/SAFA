package edu.nd.crc.safa.utilities;

import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import edu.nd.crc.safa.constants.ProjectPaths;
import edu.nd.crc.safa.entities.Project;
import edu.nd.crc.safa.output.error.ServerError;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.json.JSONException;
import org.json.JSONObject;

/**
 * Responsible for reading CSV files and validating them
 * while mindful that casing does not matter.
 */
public class FileUtilities {

    public static CSVParser readCSVFile(Project project, String fileName) throws ServerError {
        try {
            String pathToFile = ProjectPaths.getPathToFlatFile(project, fileName);
            Reader in = new FileReader(pathToFile);
            CSVFormat fileFormat = CSVFormat.DEFAULT.builder().setIgnoreHeaderCase(true).build();
            in.close();
            return new CSVParser(in, fileFormat);
        } catch (IOException e) {
            throw new ServerError("Could not read CSV file: " + fileName);
        }
    }

    public static void assertHasColumns(CSVParser file, String[] names) throws ServerError {
        List<String> headerNames = file.getHeaderNames();
        List<String> headerNamesLower = toLowerCase(headerNames);

        for (String n : names) {
            if (!headerNamesLower.contains(n)) {
                throw new ServerError("Expected file to column: " + n + " but only saw " + file.getHeaderNames());
            }
        }
    }

    public static String toString(Object[] a) {
        if (a == null) {
            return "null";
        }

        int iMax = a.length - 1;
        if (iMax == -1) {
            return "[]";
        }

        StringBuilder b = new StringBuilder();
        b.append('[');
        for (int i = 0; ; i++) {
            b.append(String.valueOf(a[i]));
            if (i == iMax) {
                return b.append(']').toString();
            }
            b.append(", ");
        }
    }

    private static List<String> toLowerCase(List<String> words) {
        List<String> result = new ArrayList<>();
        for (String word : words) {
            result.add(word.toLowerCase());
        }
        return result;
    }

    public static JSONObject toLowerCase(JSONObject jsonObject) throws JSONException {
        JSONObject result = new JSONObject();
        Iterator keys = jsonObject.keys();

        while (keys.hasNext()) {
            String key = keys.next().toString();
            Object value = jsonObject.get(key);
            if (value instanceof JSONObject) {
                result.put(key.toLowerCase(), toLowerCase((JSONObject) value));
            } else {
                result.put(key.toLowerCase(), value);
            }

        }
        return result;
    }
}
