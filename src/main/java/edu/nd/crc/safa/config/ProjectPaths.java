package edu.nd.crc.safa.config;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.UUID;

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
    public static final String PATH_TO_DEFAULT_PROJECT = ProjectPaths.PATH_TO_TEST_RESOURCES + "/before";
    public static final String PATH_TO_MINI_FILES = ProjectPaths.PATH_TO_TEST_RESOURCES + "/mini";
    public static final String PATH_TO_AFTER_FILES = ProjectPaths.PATH_TO_TEST_RESOURCES + "/after";
    public static final String PATH_TO_TEST_2 = ProjectPaths.PATH_TO_TEST_RESOURCES + "/test2";
    public static final String PATH_TO_TEST_3 = ProjectPaths.PATH_TO_TEST_RESOURCES + "/test3";

    // Jira
    public static final String PATH_TO_DRONE_ISSUES = ProjectPaths.PATH_TO_TEST_RESOURCES + "/jira/drone_response.json";

    public static String joinPaths(String... paths) {
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

        String pathToLocalStorage = joinPaths(ProjectPaths.PATH_TO_STORAGE, project.getProjectId().toString());
        if (!Files.exists(Paths.get(pathToLocalStorage)) && createIfEmpty) {
            try {
                Files.createDirectories(Paths.get(pathToLocalStorage));
            } catch (IOException e) {
                throw new RuntimeException("Could not create local storage for project: " + project.getProjectId());
            }
        }
        return pathToLocalStorage;
    }

    public static String getTemporaryPath() throws IOException {
        String randomId = UUID.randomUUID().toString();
        String pathToTemporary = joinPaths(ProjectPaths.PATH_TO_STORAGE, randomId);
        Files.createDirectories(Paths.get(pathToTemporary));
        return pathToTemporary;
    }

    public static String getPathToUploadedFiles(Project project) {
        return joinPaths(getPathToStorage(project), "uploaded");
    }

    public static String getPathToProjectFile(Project project, String fileName) {
        return joinPaths(getPathToStorage(project), fileName);
    }

    public static String getPathToFlatFile(Project project, String fileName) {
        return joinPaths(getPathToUploadedFiles(project), fileName);
    }

    public static String getPathToGeneratedFiles(Project project) {
        return joinPaths(getPathToStorage(project), "generated");
    }

    public static String getPathToTemporaryFile(String fileName) throws IOException {
        return joinPaths(getTemporaryPath(), fileName);
    }

    public static String getPathToTestResources(String fileName) {
        return joinPaths(PATH_TO_DEFAULT_PROJECT, fileName);
    }
}
