package edu.nd.crc.safa.utilities;

import java.io.File;
import java.io.IOException;

import edu.nd.crc.safa.server.messages.ServerError;

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
     * @throws ServerError failure to delete any files or folders with
     *                     directory will be thrown.
     */
    public static void clearOrCreateDirectory(String pathToDir) throws ServerError {
        File myDir = new File(pathToDir);

        if (!myDir.exists()) {
            if (!myDir.mkdirs()) {
                throw new ServerError(String.format("creating folder at path: %s", pathToDir));
            }
        }

        try {
            FileUtils.cleanDirectory(myDir);
        } catch (IOException e) {
            throw new ServerError("Could not clear directory", e);
        }
    }

    /**
     * Deletes file or folder located at given path
     *
     * @param path path to a file or directory which to delete
     * @throws ServerError fails if an error occurs while deleting file, directory,
     *                     or children of directory
     */
    public static void deletePath(String path) throws ServerError {
        File objectAtPath = new File(path);

        if (objectAtPath.exists()) {
            if (objectAtPath.isDirectory()) {
                try {
                    FileUtils.deleteDirectory(objectAtPath);
                } catch (IOException e) {
                    e.printStackTrace();
                    throw new ServerError("Could not delete directory: " + path);
                }
            } else {
                if (!objectAtPath.delete()) {
                    throw new ServerError("Could not delete file at: " + path);
                }
            }
        }
    }

    private static void recursivelyDeleteDirectory(File pathToObject) throws ServerError {
        File[] files = pathToObject.listFiles();
        if (files != null) {
            for (File file : files) {
                recursivelyDeleteDirectory(file);
            }
        }
        if (!pathToObject.delete()) {
            throw new ServerError("Could not delete requested file: " + pathToObject);
        }
    }
}
