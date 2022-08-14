package edu.nd.crc.safa.utilities;

import java.io.File;
import java.io.IOException;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.apache.commons.io.FileUtils;

/**
 * Responsible for encapsulating common operating system
 * primarily surrounding file manipulation.
 */
@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class OSHelper {

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

        if (!myDir.exists() && !myDir.mkdirs()) {
            throw new SafaError("creating folder at path: %s", pathToDir);
        }

        FileUtils.cleanDirectory(myDir);
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
}
