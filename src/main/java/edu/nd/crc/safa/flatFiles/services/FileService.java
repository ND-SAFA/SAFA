package edu.nd.crc.safa.flatFiles.services;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;
import javax.servlet.http.HttpServletResponse;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.utilities.OSHelper;

import lombok.AllArgsConstructor;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Service;
import org.springframework.util.StreamUtils;
import org.springframework.web.multipart.MultipartFile;

/**
 * Responsible for exposing an API for uploading,
 * parsing, and deleting flat files.
 */
@Service
@Scope("singleton")
@AllArgsConstructor
public class FileService {

    /**
     * Uploads given files to disk and associates them with given project.
     *
     * @param project      The project whose files are related to.
     * @param requestFiles The files being stored on the server.
     * @throws SafaError Throws error if error occurs while creating necessary directory structure or writing to disk.
     */
    public void uploadFilesToServer(Project project, List<MultipartFile> requestFiles) throws SafaError {
        String pathToStorage = ProjectPaths.getPathToUploadedFiles(project);
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

    /**
     * Streams zip file containing given files as response.
     *
     * @param response    The server response to stream the zip file to.
     * @param zipFileName The name of the zip file.
     * @param files       The files to zip and stream.
     * @throws IOException Throws exception if error occurs while opening any of the files.
     */
    public void sendFilesAsZipResponse(HttpServletResponse response,
                                       String zipFileName,
                                       List<File> files) throws IOException {
        String contentDisposition = String.format("attachment; filename=%s", zipFileName);
        response.setContentType("application/zip");
        response.setHeader("Content-Disposition", contentDisposition);
        ZipOutputStream zipOutputStream = new ZipOutputStream(response.getOutputStream());
        for (File file : files) {
            InputStream targetStream = new FileInputStream(file);

            ZipEntry zipEntry = new ZipEntry(file.getName());
            zipEntry.setSize(file.length());
            zipEntry.setTime(System.currentTimeMillis());

            zipOutputStream.putNextEntry(zipEntry);

            StreamUtils.copy(targetStream, zipOutputStream);
            zipOutputStream.closeEntry();
        }
        zipOutputStream.finish();
    }
}
