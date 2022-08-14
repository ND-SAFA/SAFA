package edu.nd.crc.safa.utilities;

import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Objects;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;

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

    public static CSVParser readCSVFile(String pathToFile) throws IOException {
        File csvData = new File(pathToFile);
        if (!csvData.exists()) {
            String errorMessage = String.format("Cannot find CSV file %s.", csvData.getName());
            throw new IOException(errorMessage);
        }

        CSVFormat fileFormat = createUnknownHeaderCsvFileFormat();
        return CSVParser.parse(csvData, Charset.defaultCharset(), fileFormat);
    }

    public static CSVParser readMultiPartCSVFile(MultipartFile file, String[] requiredColumns) throws
        SafaError {
        if (!Objects.requireNonNull(file.getOriginalFilename()).contains(".csv")) {
            throw new SafaError("Expected a CSV file with columns: %s", (Object) requiredColumns);
        }
        try {
            CSVParser parsedFile = CSVParser.parse(new String(file.getBytes()), createUnknownHeaderCsvFileFormat());
            assertHasColumns(parsedFile, requiredColumns);
            return parsedFile;
        } catch (IOException e) {
            throw new SafaError("Unable to read csv file %s.", file.getOriginalFilename());
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
                throw new SafaError("Expected CSV to have column(s) %s but found: %s",
                    requiredColumnsLabel,
                    file.getHeaderNames());
            }
        }
    }

    public static void assertHasKeys(JSONObject obj, List<String> keys) throws SafaError {
        for (String key : keys) {
            if (!obj.has(key)) {
                throw new SafaError("Expected %s to have key: %s", obj, key);
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
        String temporaryFolder = ProjectPaths.Storage.createTemporaryDirectory();
        List<File> filesCreated = new ArrayList<>();
        while ((entry = zin.getNextEntry()) != null) {
            String name = entry.getName();
            String pathToFile = builtPath(temporaryFolder, name);
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

    /**
     * Writes content to file.
     *
     * @param file        The file to write to.
     * @param fileContent The content to write to file.
     * @throws IOException Throws error if problem opening file.
     */
    public static void writeToFile(File file, String fileContent) throws IOException {
        try (FileWriter myWriter = new FileWriter(file)) {
            myWriter.write(fileContent);
        }
    }

    /**
     * Attempts to create directory to given path.
     *
     * @param pathToDirectory Path to directory to create.
     * @param createIfEmpty   Flag used to disable attempt
     */
    public static void createDirectoryIfEmpty(String pathToDirectory, boolean createIfEmpty) throws IOException {
        if (createIfEmpty) {
            createDirectoryIfEmpty(pathToDirectory);
        }
    }

    /**
     * Creates directory at given path if it does not exist.
     *
     * @param pathToDirectory Path to directory to create.
     * @throws IOException If error occurs while creating directory.
     */
    public static void createDirectoryIfEmpty(String pathToDirectory) throws IOException {
        if (!Files.exists(Paths.get(pathToDirectory))) {
            Files.createDirectories(Paths.get(pathToDirectory));
        }
    }

    /**
     * Creates OS-aware path of given directory.
     *
     * @param directories Directories that once joined create path.
     * @return String representing built path.
     */
    public static String builtPath(String... directories) {
        StringBuilder finalPath = new StringBuilder();
        for (int i = 0; i < directories.length; i++) {
            String p = directories[i];
            if (i < directories.length - 1) {
                finalPath.append(p).append(File.separator);
            } else {
                finalPath.append(p);
            }
        }
        return finalPath.toString();
    }
}
