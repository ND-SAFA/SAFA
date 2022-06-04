package edu.nd.crc.safa.config;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

import edu.nd.crc.safa.server.entities.db.Project;

/**
 * Contains common full paths used through app.
 */
public class ProjectPaths {
    // Flat files
    public static final String PATH_TO_ROOT = System.getProperty("user.dir");
    public static final String PATH_TO_BUILD = ProjectPaths.PATH_TO_ROOT + "/build";
    public static final String PATH_TO_STORAGE = ProjectPaths.PATH_TO_BUILD + "/storage";
    public static final String PATH_TO_RESOURCES = ProjectPaths.PATH_TO_ROOT + "/resources";
    public static final String PATH_TO_TEST_RESOURCES = ProjectPaths.PATH_TO_RESOURCES + "/tests";
    public static final String PATH_TO_BEFORE_FILES = ProjectPaths.PATH_TO_TEST_RESOURCES + "/before";
    public static final String PATH_TO_MINI_FILES = ProjectPaths.PATH_TO_TEST_RESOURCES + "/mini";
    public static final String PATH_TO_AFTER_FILES = ProjectPaths.PATH_TO_TEST_RESOURCES + "/after";
    public static final String PATH_TO_TEST_2 = ProjectPaths.PATH_TO_TEST_RESOURCES + "/test2";
    public static final String PATH_TO_TEST_3 = ProjectPaths.PATH_TO_TEST_RESOURCES + "/test3";

    // Jira
    public static final String PATH_TO_DRONE_ISSUES = ProjectPaths.PATH_TO_TEST_RESOURCES + "/jira/drone_response.json";

    private static String pathHelper(String... paths) {
        StringBuilder finalPath = new StringBuilder();
        for (int i = 0; i < paths.length; i++) {
            String p = paths[i];
            if (i < paths.length - 1) {
                finalPath.append(p).append(File.separator);
            } else {
                finalPath.append(p);
            }
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

    public static String getPathToTestResources(String fileName) {
        return pathHelper(PATH_TO_BEFORE_FILES, fileName);
    }
}
