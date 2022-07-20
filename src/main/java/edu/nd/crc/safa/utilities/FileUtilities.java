package edu.nd.crc.safa.utilities;

import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Objects;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.api.SafaError;

import lombok.NoArgsConstructor;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.io.FileUtils;
import org.json.JSONException;
import org.json.JSONObject;
import org.springframework.web.multipart.MultipartFile;

/**
 * Responsible for reading CSV files and validating them
 * while mindful that casing does not matter.
 */
@NoArgsConstructor
public class FileUtilities {

    public static CSVParser readCSVFile(String pathToFile) throws SafaError {
        try {
            File csvData = new File(pathToFile);
            if (!csvData.exists()) {
                throw new SafaError("CSV file does not exist: " + pathToFile);
            }

            CSVFormat fileFormat = getCSVFormat();
            return CSVParser.parse(csvData, Charset.defaultCharset(), fileFormat);
        } catch (IOException e) {
            String error = String.format("Could not read CSV file at path: %s", pathToFile);
            throw new SafaError(error, e);
        }
    }

    public static CSVParser readMultiPartCSVFile(MultipartFile file, String[] requiredColumns) throws
        SafaError {
        String requiredColumnsLabel = String.join(", ", requiredColumns);
        if (!Objects.requireNonNull(file.getOriginalFilename()).contains(".csv")) {
            throw new SafaError("Expected a CSV file with columns: " + requiredColumnsLabel);
        }
        try {
            CSVParser parsedFile = CSVParser.parse(new String(file.getBytes()), getCSVFormat());
            assertHasColumns(parsedFile, requiredColumns);
            return parsedFile;
        } catch (IOException e) {
            String error = "Unable to read csv file: " + file.getOriginalFilename();
            throw new SafaError(error, e);
        }
    }

    public static JSONObject readMultiPartJSONFile(MultipartFile file) throws IOException {
        return new JSONObject(new String(file.getBytes()));
    }

    public static CSVFormat getCSVFormat() {
        return CSVFormat.DEFAULT
            .withHeader() // only way to read headers without defining them.
            .builder()
            .setSkipHeaderRecord(false)
            .setIgnoreEmptyLines(true)
            .setAllowMissingColumnNames(true)
            .setIgnoreHeaderCase(true)
            .build();
    }

    public static void assertHasColumns(CSVParser file, String[] requiredColumns) throws SafaError {
        List<String> headerNames = file.getHeaderNames();
        List<String> headerNamesLower = toLowerCase(headerNames);

        for (String rColumn : requiredColumns) {
            if (!headerNamesLower.contains(rColumn)) {
                String requiredColumnsLabel = String.join(", ", requiredColumns);
                String error = "Expected CSV to have column(s) [%s] but found: %s";
                throw new SafaError(String.format(error, requiredColumnsLabel, file.getHeaderNames()));
            }
        }
    }

    public static void assertHasKeys(JSONObject obj, String[] keys) throws SafaError {
        for (String key : keys) {
            if (!obj.has(key)) {
                String error = String.format("Expected %s to have key: %s", obj, key);
                throw new SafaError(error);
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

    /**
     * Returns the JSONObject parsed from path to JSON file.
     *
     * @param path The path to the JSON file.
     * @return JSONObject
     * @throws IOException If file is missing or not able to be read.
     */
    public static JSONObject readJSONFile(String path) throws IOException {
        String fileContent = FileUtils.readFileToString(new File(path), "utf-8");
        return new JSONObject(fileContent);
    }

    public static List<File> getZipFiles(String content) throws IOException {
        ZipEntry entry;
        final var zin = new ZipInputStream(new ByteArrayInputStream(content.getBytes(StandardCharsets.UTF_8)));
        String temporaryFolder = ProjectPaths.getTemporaryPath();
        List<File> filesCreated = new ArrayList<>();
        while ((entry = zin.getNextEntry()) != null) {
            String name = entry.getName();
            String pathToFile = ProjectPaths.joinPaths(temporaryFolder, name);
            try (FileOutputStream outputStream = new FileOutputStream(pathToFile)) {
                for (var c = zin.read(); c != -1; c = zin.read()) {
                    outputStream.write(c);
                }
                outputStream.flush();
                zin.closeEntry();
                filesCreated.add(new File(pathToFile));
            }
        }
        return filesCreated;
    }


}
