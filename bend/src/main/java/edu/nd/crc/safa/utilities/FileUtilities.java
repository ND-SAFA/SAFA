package edu.nd.crc.safa.utilities;

import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.PathMatcher;
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
    public static final String URL_SEP = "/";

    public static final PathMatcher[] CODE_MATCHERS = {
        FileSystems.getDefault().getPathMatcher(
            "glob:*.{"
            + "asm,"
            + "c,"
            + "cc,"
            + "cfg,"
            + "cmake,"
            + "cpp,"
            + "cs,"
            + "css,"
            + "cxx,"
            + "dart,"
            + "glsl,"
            + "go,"
            + "h,"
            + "hpp,"
            + "htm,"
            + "html,"
            + "hxx,"
            + "ipynb,"
            + "java,"
            + "js,"
            + "json,"
            + "jsx,"
            + "kt,"
            + "php,"
            + "py,"
            + "rb,"
            + "resx,"
            + "s,"
            + "sass,"
            + "scss,"
            + "sh,"
            + "sql,"
            + "swift,"
            + "ts,"
            + "tsx,"
            + "vue,"
            + "vb,"
            + "xml,"
            + "yaml,"
            + "yml"
            + "}"),
        FileSystems.getDefault().getPathMatcher("glob:CMakeLists.txt"),
        FileSystems.getDefault().getPathMatcher("glob:.gitignore"),
        FileSystems.getDefault().getPathMatcher("glob:.gitmodules")
    };

    public static CSVParser readCSVFile(String pathToFile) throws IOException {
        File csvData = new File(pathToFile);
        if (!csvData.exists()) {
            String errorMessage = String.format("Could not find CSV file %s.", csvData.getAbsolutePath());
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
            String pathToFile = buildPath(temporaryFolder, name);
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
    public static String buildPath(String... directories) {
        return String.join(File.separator, directories);
    }

    /**
     * Creates a URL by combining given parts.
     *
     * @param directories Directories that once joined create path.
     * @return String representing built path.
     */
    public static String buildUrl(String... directories) {
        return String.join(URL_SEP, directories);
    }

    /**
     * Deletes file or folder located at given path
     *
     * @param path path to a file or directory which to delete
     * @throws SafaError If an error occurs while deleting file, directory, or children of directory.
     */
    public static void deletePath(String path) throws SafaError, IOException {
        File objectAtPath = new File(path);

        if (objectAtPath.exists()) {
            if (objectAtPath.isDirectory()) {
                FileUtils.deleteDirectory(objectAtPath);
            } else {
                if (!objectAtPath.delete()) {
                    String errorMessage = String.format("Could not delete file at: %s", path);
                    throw new IOException(errorMessage);
                }
            }
        }
    }

    /**
     * Removes any children of given directory includes
     * all sub-folders and files. If directory has not
     * been created then new directory is created.
     *
     * @param pathToDir path to a directory
     * @throws SafaError If failure to delete any files or folders.
     */
    public static void clearOrCreateDirectory(String pathToDir) throws IOException {
        File myDir = new File(pathToDir);

        if (!myDir.exists()) {
            myDir.mkdirs();
        }

        FileUtils.cleanDirectory(myDir);
    }

    /**
     * Reads a file that is located in the classpath (i.e. in the resources folder)
     * and returns the contents of the file as a string.
     *
     * @param path Path to the file (relative to the resources folder).
     * @return The contents of the file.
     * @throws IOException If the file could not be read.
     */
    public static String readClasspathFile(String path) throws IOException {
        ClassLoader classLoader = FileUtilities.class.getClassLoader();

        try (InputStream in = classLoader.getResourceAsStream(path)) {
            assert in != null;
            return new String(in.readAllBytes());
        }
    }

    /**
     * Returns whether a filename represents a code file type that we are aware of.
     *
     * @param path The path of the file
     * @return Whether the file is a code file
     */
    public static boolean isCodeFile(Path path) {
        Path filename = path.getFileName();
        for (PathMatcher matcher : CODE_MATCHERS) {
            if (matcher.matches(filename)) {
                return true;
            }
        }
        return false;
    }
}
