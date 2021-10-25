package edu.nd.crc.safa.utilities;

import java.io.File;
import java.io.IOException;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import edu.nd.crc.safa.server.messages.ServerError;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.json.JSONException;
import org.json.JSONObject;

/**
 * Responsible for reading CSV files and validating them
 * while mindful that casing does not matter.
 */
public class FileUtilities {

    public static CSVParser readCSVFile(String pathToFile) throws ServerError {
        try {
            File csvData = new File(pathToFile);
            if (!csvData.exists()) {
                throw new ServerError("CSV file does not exist: " + pathToFile);
            }

            CSVFormat fileFormat = CSVFormat.DEFAULT
                .withHeader() // only way to read headers without defining them.
                .builder()
                .setSkipHeaderRecord(false)
                .setIgnoreEmptyLines(true)
                .setAllowMissingColumnNames(true)
                .setIgnoreHeaderCase(true)
                .build();

            return CSVParser.parse(csvData, Charset.defaultCharset(), fileFormat);
        } catch (IOException e) {
            String error = String.format("Could not read CSV file at path: %s", pathToFile);
            throw new ServerError(error, e);
        }
    }

    public static void assertHasColumns(CSVParser file, String[] names) throws ServerError {
        List<String> headerNames = file.getHeaderNames();
        List<String> headerNamesLower = toLowerCase(headerNames);

        for (String n : names) {
            if (!headerNamesLower.contains(n)) {
                String error = "Expected file to have column [%s] but only saw %s";
                throw new ServerError(String.format(error, n, file.getHeaderNames()));
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
            b.append(a[i]);
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
