package edu.nd.crc.safa.utilities;

import java.io.IOException;
import java.util.Arrays;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.services.FileUploadService;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.springframework.web.multipart.MultipartFile;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class FlatFileUtility {
    /**
     * Uploads files to project directory path.
     *
     * @param serviceProvider Provides access to app services.
     * @param project         The project to store files for.
     * @param files           The files to store.
     * @return Path to project directory.
     * @throws IOException Throws exception if error occurs while moving files.
     */
    public static String uploadFlatFiles(ServiceProvider serviceProvider, Project project, MultipartFile[] files)
        throws IOException {
        String projectDirectoryPath = ProjectPaths.Storage.projectPath(project, true);
        FileUploadService fileUploadService = serviceProvider.getFileUploadService();
        fileUploadService.uploadFilesToServer(project, Arrays.asList(files));
        return projectDirectoryPath;
    }
}
