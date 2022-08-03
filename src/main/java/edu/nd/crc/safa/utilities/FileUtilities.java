package edu.nd.crc.safa.utilities;

import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileWriter;
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

import lombok.AccessLevel;
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
@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class FileUtilities {

    public static CSVParser readCSVFile(String pathToFile) throws SafaError {
        try {
            File csvData = new File(pathToFile);
            if (!csvData.exists()) {
                throw new SafaError("CSV file does not exist: " + pathToFile);
            }

            CSVFormat fileFormat = createUnknownHeaderCsvFileFormat();
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
            CSVParser parsedFile = CSVParser.parse(new String(file.getBytes()), createUnknownHeaderCsvFileFormat());
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

    public static CSVFormat createUnknownHeaderCsvFileFormat() {
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

    public static void assertHasKeys(JSONObject obj, List<String> keys) throws SafaError {
        for (String key : keys) {
            if (!obj.has(key)) {
                String error = String.format("Expected %s to have key: %s", obj, key);
                throw new SafaError(error);
            }
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
        Iterator<String> keys = jsonObject.keys();

        while (keys.hasNext()) {
            String key = keys.next();
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
        String fileContent = FileUtils.readFileToString(new File(path), StandardCharsets.UTF_8);
        return new JSONObject(fileContent);
    }

    /**
     * Extracts files in given zip bytearray as a string.
     *
     * @param content The content of the zip as a string representing an array of bytes.
     * @return List of files found in the zip content.
     * @throws IOException Throws error if error occurred while saving file.
     */
    public static List<File> extractFilesFromZipContent(String content) throws IOException {
        ZipEntry entry;
        final var zin = new ZipInputStream(new ByteArrayInputStream(content.getBytes(StandardCharsets.ISO_8859_1)));
        String temporaryFolder = ProjectPaths.createTemporaryDirectory();
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

    public static void writeToFile(File file, String fileContent) throws IOException {
        try (FileWriter myWriter = new FileWriter(file)) {
            myWriter.write(fileContent);
        }
    }

    public void hasRequiredFields(JSONObject json, Iterator<String> fields) {
        for (Iterator<String> it = fields; it.hasNext(); ) {
            String field = it.next();
            if (!json.has(field)) {
                throw new SafaError("Expected object:\n" + json + "\n to contain field:" + field);
            }
        }
    }
}
