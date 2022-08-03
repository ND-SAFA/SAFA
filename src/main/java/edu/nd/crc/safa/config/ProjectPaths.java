package edu.nd.crc.safa.config;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.Project;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;

/**
 * Contains common paths used through app.
 */
@NoArgsConstructor(access = AccessLevel.PRIVATE)
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

    private static void createDirectoryIfEmpty(String pathToLocalStorage, boolean createIfEmpty) {
        if (createIfEmpty) {
            createDirectoryIfEmpty(pathToLocalStorage);
        }
    }

    private static void createDirectoryIfEmpty(String pathToLocalStorage) {
        if (!Files.exists(Paths.get(pathToLocalStorage))) {
            try {
                Files.createDirectories(Paths.get(pathToLocalStorage));
            } catch (IOException e) {
                throw new RuntimeException("Could not create local storage for project. \n Error: " + e.getMessage());
            }
        }
    }

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

    public static String getPathToStorage(Project project, boolean createIfEmpty) {
        String pathToLocalStorage = joinPaths(ProjectPaths.PATH_TO_STORAGE, project.getProjectId().toString());
        createDirectoryIfEmpty(pathToLocalStorage, createIfEmpty);
        return pathToLocalStorage;
    }

    public static String createTemporaryDirectory() throws IOException {
        String randomId = UUID.randomUUID().toString();
        String pathToTemporary = joinPaths(ProjectPaths.PATH_TO_STORAGE, randomId);
        Files.createDirectories(Paths.get(pathToTemporary));
        return pathToTemporary;
    }

    public static String getPathToUploadedFiles(Project project, boolean createIfEmpty) {
        String path = joinPaths(getPathToStorage(project, createIfEmpty), "uploaded");
        createDirectoryIfEmpty(path, createIfEmpty);
        return path;
    }

    public static String getPathToProjectFile(Project project, String fileName) {
        return joinPaths(getPathToStorage(project, true), fileName);
    }

    public static String getPathToFlatFile(Project project, String fileName) {
        return joinPaths(getPathToUploadedFiles(project, true), fileName);
    }

    public static String getPathToDefaultProjectFile(String fileName) {
        return joinPaths(PATH_TO_DEFAULT_PROJECT, fileName);
    }
}
