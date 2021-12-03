package edu.nd.crc.safa.utilities;

import java.io.File;
import java.io.IOException;

import edu.nd.crc.safa.server.entities.api.SafaError;

import org.apache.commons.io.FileUtils;

/**
 * Responsible for encapsulating common operating system
 * primarily surrounding file manipulation.
 */
public class OSHelper {

    /**
     * Removes any children of given directory includes
     * all sub-folders and files. If directory has not
     * been created then new directory is created.
     *
     * @param pathToDir path to a directory
     * @throws SafaError failure to delete any files or folders with
     *                   directory will be thrown.
     */
    public static void clearOrCreateDirectory(String pathToDir) throws SafaError {
        File myDir = new File(pathToDir);

        if (!myDir.exists()) {
            if (!myDir.mkdirs()) {
                throw new SafaError(String.format("creating folder at path: %s", pathToDir));
            }
        }

        try {
            FileUtils.cleanDirectory(myDir);
        } catch (IOException e) {
            String error = String.format("Could not clear directory at path: %s", pathToDir);
            throw new SafaError(error, e);
        }
    }

    /**
     * Deletes file or folder located at given path
     *
     * @param path path to a file or directory which to delete
     * @throws SafaError fails if an error occurs while deleting file, directory,
     *                   or children of directory
     */
    public static void deletePath(String path) throws SafaError {
        File objectAtPath = new File(path);

        if (objectAtPath.exists()) {
            if (objectAtPath.isDirectory()) {
                try {
                    FileUtils.deleteDirectory(objectAtPath);
                } catch (IOException e) {
                    e.printStackTrace();
                    throw new SafaError("Could not delete directory: " + path);
                }
            } else {
                if (!objectAtPath.delete()) {
                    throw new SafaError("Could not delete file at: " + path);
                }
            }
        }
    }
}
