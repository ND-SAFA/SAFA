package edu.nd.crc.safa.constants;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

import edu.nd.crc.safa.entities.Project;

/**
 * Contains common full paths used through app.
 */
public class ProjectPaths {
    public static final String PATH_TO_ROOT = System.getProperty("user.dir");
    public static final String PATH_TO_BUILD = PATH_TO_ROOT + "/build";
    public static final String PATH_TO_STORAGE = PATH_TO_BUILD + "/storage";
    public static final String PATH_TO_TEST_RESOURCES = PATH_TO_ROOT + "/resources";

    private static String pathHelper(String... paths) {
        StringBuilder finalPath = new StringBuilder();
        for (String p : paths) {
            finalPath.append(p).append(File.separator);
        }
        return finalPath.toString();
    }

    public static String getPathToStorage(Project project) {
        return getPathToStorage(project, true);
    }

    public static String getPathToStorage(Project project, boolean createIfEmpty) {

        String pathToLocalStorage = pathHelper(ProjectPaths.PATH_TO_STORAGE, project.getProjectId().toString());
        if (!Files.exists(Paths.get(pathToLocalStorage)) && createIfEmpty) {
            try {
                Files.createDirectories(Paths.get(pathToLocalStorage));
            } catch (IOException e) {
                throw new RuntimeException("Could not create local storage for project: " + project.getProjectId());
            }
        }
        return pathToLocalStorage;
    }

    public static String getPathToUploadedFiles(Project project) {
        return pathHelper(getPathToStorage(project), "uploaded");
    }

    public static String getPathToFlatFile(Project project, String fileName) {
        return pathHelper(getPathToUploadedFiles(project), fileName);
    }

    public static String getPathToGeneratedFiles(Project project) {
        return pathHelper(getPathToStorage(project), "generated");
    }

    public static String getPathToGeneratedFile(Project project, String fileName) {
        return pathHelper(getPathToGeneratedFiles(project), fileName);
    }
}
