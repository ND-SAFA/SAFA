package edu.nd.crc.safa.features.flatfiles.services;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.List;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

import jakarta.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Service;
import org.springframework.util.StreamUtils;

/**
 * Creates and sends zip files over HTTP.
 */
@Service
public class ZipFileService {
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
            try (InputStream targetStream = new FileInputStream(file)) {
                ZipEntry zipEntry = new ZipEntry(file.getName());
                zipEntry.setSize(file.length());
                zipEntry.setTime(System.currentTimeMillis());

                zipOutputStream.putNextEntry(zipEntry);

                StreamUtils.copy(targetStream, zipOutputStream);
                zipOutputStream.closeEntry();
            }
        }
        zipOutputStream.finish();
    }
}
