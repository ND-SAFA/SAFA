package edu.nd.crc.safa.builders;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

import lombok.NoArgsConstructor;
import org.apache.commons.io.FileUtils;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.web.multipart.MultipartFile;

/**
 * Creates a test layer for sending multi-part file http requests.
 */
@NoArgsConstructor
public class MultipartRequestService {

    public static List<MockMultipartFile> createMockMultipartFilesFromDirectory(String pathToDirectory,
                                                                                String attributeName)
        throws IOException {
        File directory = new File(pathToDirectory);
        List<MockMultipartFile> files = new ArrayList<>();
        File[] subFiles = directory.listFiles();

        if (subFiles == null) {
            throw new RuntimeException("Could not list files inside directory: " + pathToDirectory);
        }

        for (File subFile : subFiles) {
            files.add(createFile(subFile.getAbsolutePath(), attributeName));
        }
        return files;
    }

    public static MockMultipartFile createFile(String pathToFile, String attributeName) throws IOException {
        File file = new File(pathToFile);
        byte[] fileContent = FileUtils.readFileToByteArray(file);
        return new MockMultipartFile(
            attributeName,
            file.getName(),
            Files.probeContentType(Paths.get(pathToFile)),
            fileContent);
    }

    public static List<MultipartFile> createMultipartFilesFromDirectory(String pathToDirectory, String attributeName)
        throws IOException {
        List<MockMultipartFile> mocks = createMockMultipartFilesFromDirectory(pathToDirectory, attributeName);
        return new ArrayList<>(mocks);
    }
}
