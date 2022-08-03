package edu.nd.crc.safa.flatfiles.services;

import java.io.File;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.utilities.OSHelper;

import lombok.AllArgsConstructor;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

/**
 * Responsible for exposing an API for uploading,
 * parsing, and deleting flat files.
 */
@Service
@Scope("singleton")
@AllArgsConstructor
public class FileUploadService {

    /**
     * Uploads given files to disk and associates them with given project.
     *
     * @param project      The project whose files are related to.
     * @param requestFiles The files being stored on the server.
     * @throws SafaError Throws error if error occurs while creating necessary directory structure or writing to disk.
     */
    public void uploadFilesToServer(Project project, List<MultipartFile> requestFiles) throws SafaError {
        String pathToStorage = ProjectPaths.getPathToUploadedFiles(project, true);
        OSHelper.clearOrCreateDirectory(pathToStorage);

        for (MultipartFile requestFile : requestFiles) {
            try {
                String pathToFile = ProjectPaths.getPathToFlatFile(project, requestFile.getOriginalFilename());
                Path pathToUploadedFile = Paths.get(pathToFile);
                File newFile = new File(pathToUploadedFile.toString());
                File parentFile = newFile.getParentFile();
                parentFile.mkdirs();
                newFile.createNewFile();
                requestFile.transferTo(newFile);
            } catch (IOException e) {
                String error = String.format("Could not upload file: %s", requestFile.getOriginalFilename());
                e.printStackTrace();
                throw new SafaError(error, e);
            }
        }
    }
}
