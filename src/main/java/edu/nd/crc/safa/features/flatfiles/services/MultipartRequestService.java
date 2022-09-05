package edu.nd.crc.safa.features.flatfiles.services;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import org.apache.commons.io.FileUtils;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.web.multipart.MultipartFile;

/**
 * Creates a test layer for sending multi-part file http requests.
 */
public interface MultipartRequestService {

    /**
     * Reads files in directory and converts them to MultipartFiles.
     *
     * @param pathToDirectory Path to directory whose files are read.
     * @param attributeName   Name of the attribute in the request body to group files under. \See
     *                        readAsMockMultipartFile for more information
     * @return MultipartFiles read from directory.
     * @throws IOException Throws errors if any errors occur while reading mock files.
     */
    static List<MultipartFile> readDirectoryAsMultipartFiles(String pathToDirectory, String attributeName)
        throws IOException {
        List<MockMultipartFile> mocks = readDirectoryAsMockMultipartFiles(pathToDirectory, attributeName);
        return new ArrayList<>(mocks);
    }

    /**
     * Reads files in directory and converts them to MockMultipartFiles.
     *
     * @param pathToDirectory Path the directory whose files are read.
     * @param attributeName   Name of the attribute in the request body to group files under.
     *                        See readAsMockMultipartFile for more information
     * @return MockMultipartFile read from directory.
     * @throws IOException Throws errors if any errors occur while reading mock files.
     */
    static List<MockMultipartFile> readDirectoryAsMockMultipartFiles(String pathToDirectory,
                                                                     String attributeName)
        throws IOException {
        File directory = new File(pathToDirectory);
        return convertToMockMultipartFiles(getFilesInDirectory(directory), attributeName);
    }

    static List<MockMultipartFile> convertToMockMultipartFiles(File[] files, String attributeName) throws IOException {
        return convertToMockMultipartFiles(Arrays.asList(files), attributeName);
    }

    static List<MockMultipartFile> convertToMockMultipartFiles(Iterable<File> files,
                                                               String attributeName) throws IOException {
        List<MockMultipartFile> mockMultipartFiles = new ArrayList<>();
        for (File subFile : files) {
            mockMultipartFiles.add(readAsMockMultipartFile(subFile.getAbsolutePath(), attributeName));
        }
        return mockMultipartFiles;
    }

    /**
     * Reads file and converts it to a mock multi-part file.
     *
     * @param pathToFile         Path to file to read
     * @param paramNameInRequest Name of the parameter containing this file. Note, this is useful for sending
     *                           multiple files in a single parameter. Parameter groupings are defined using
     *                           this given name.
     *                           object use the filename to group them together as a parameter.
     * @return File as a MockMultipartField
     * @throws IOException If file cannot be read.
     */
    static MockMultipartFile readAsMockMultipartFile(String pathToFile, String paramNameInRequest)
        throws IOException {
        File file = new File(pathToFile);
        byte[] fileContent = FileUtils.readFileToByteArray(file);
        return new MockMultipartFile(
            paramNameInRequest,
            file.getName(),
            Files.probeContentType(Paths.get(pathToFile)),
            fileContent);
    }

    static MockMultipartFile readAsMultipartFile(String pathToFile, String paramNameInRequest)
        throws IOException {
        File file = new File(pathToFile);
        byte[] fileContent = FileUtils.readFileToByteArray(file);
        return new MockMultipartFile(
            paramNameInRequest,
            file.getName(),
            Files.probeContentType(Paths.get(pathToFile)),
            fileContent);
    }

    private static File[] getFilesInDirectory(File directory) {
        File[] directoryFiles = directory.listFiles();

        if (directoryFiles == null) {
            throw new SafaError("Could not list files inside directory: %s", directory.getPath());
        }
        return directoryFiles;
    }
}
