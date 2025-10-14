package edu.nd.crc.safa.features.users.services;

import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.services.MultipartRequestService;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@AllArgsConstructor
@Service
public class DefaultProjectCreatorService {
    /**
     * Creates project from flat files of project directory for user.
     *
     * @param projectDir      Path to directory containing flat files.
     * @param serviceProvider Provides persistent services.
     * @throws IOException If error occurs while reading default project.
     */
    public void createProjectForUser(String projectDir,
                                     ServiceProvider serviceProvider) throws IOException {
        List<MultipartFile> defaultProjectFiles = MultipartRequestService
            .readDirectoryAsMultipartFiles(projectDir, "files");
        MultipartFile[] defaultProjectFilesArray = new MultipartFile[defaultProjectFiles.size()];
        defaultProjectFiles.toArray(defaultProjectFilesArray);

    }
}
