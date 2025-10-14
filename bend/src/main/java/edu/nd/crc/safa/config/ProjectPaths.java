package edu.nd.crc.safa.config;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.UUID;

import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.utilities.FileUtilities;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;

/**
 * Contains common paths used through app.
 */
@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class ProjectPaths {
    // Flat files
    public static final String ROOT = System.getProperty("user.dir");
    public static final String BUILD = ProjectPaths.ROOT + "/build";

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Storage {

        public static final String PATH = ProjectPaths.BUILD + "/storage";

        public static String createTemporaryDirectory() throws IOException {
            String randomId = UUID.randomUUID().toString();
            String pathToTemporary = FileUtilities.buildPath(Storage.PATH, randomId);
            Files.createDirectories(Paths.get(pathToTemporary));
            return pathToTemporary;
        }

        public static String getStorageRelativePath(String fullPath) {
            Path path = Path.of(fullPath);
            Path storagePath = Path.of(PATH);
            return storagePath.relativize(path).toString();
        }

        public static String getPathToProjectFile(Project project, String fileName) throws IOException {
            String projectPath = Storage.projectPath(project, false);
            return getPathToProjectFile(projectPath, fileName);
        }

        public static String getPathToProjectFile(String projectFolder, String fileName) throws IOException {
            return FileUtilities.buildPath(Storage.projectPath(projectFolder, true), fileName);
        }

        public static String uploadedProjectFilePath(Project project, String fileName) throws IOException {
            String projectPath = Storage.projectPath(project, false);
            return uploadedProjectFilePath(projectPath, fileName);
        }

        public static String uploadedProjectFilePath(String projectFolder, String fileName) throws IOException {
            return FileUtilities.buildPath(projectUploadsPath(projectFolder, true), fileName);
        }

        public static String projectUploadsPath(Project project, boolean createIfEmpty) throws IOException {
            String projectPath = Storage.projectPath(project, createIfEmpty);
            return projectUploadsPath(projectPath, createIfEmpty);
        }

        public static String projectUploadsPath(String projectFolder, boolean createIfEmpty) throws IOException {
            String path = FileUtilities.buildPath(projectFolder, "uploaded");
            FileUtilities.createDirectoryIfEmpty(path, createIfEmpty);
            return path;
        }

        public static String projectPath(Project project, boolean createIfEmpty) throws IOException {
            return projectPath(project.getProjectId().toString(), createIfEmpty);
        }

        public static String projectPath(String projectFolder, boolean createIfEmpty) throws IOException {
            String pathToLocalStorage = FileUtilities.buildPath(Storage.PATH, projectFolder);
            FileUtilities.createDirectoryIfEmpty(pathToLocalStorage, createIfEmpty);
            return pathToLocalStorage;
        }
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Resources {
        public static final String BASE = ProjectPaths.ROOT + "/resources";

        @NoArgsConstructor(access = AccessLevel.PRIVATE)
        public static class Tests {
            protected static final String PATH = ProjectPaths.Resources.BASE + "/tests"; // PRIVATE scope results in
            // null path
            public static final String MINI = PATH + "/mini";
            public static final String TEST2 = PATH + "/test2";
            public static final String TEST3 = PATH + "/test3";
            public static final String MISSING_DATA_FILE = PATH + "/missing_data_file";
            public static final String CUSTOM_ATTRIBUTES_CSV = PATH + "/custom_attributes_csv";
            public static final String CUSTOM_ATTRIBUTES_JSON = PATH + "/custom_attributes_json";
            public static final String DRONE_SLICE = PATH + "/DroneSlice";

            @NoArgsConstructor(access = AccessLevel.PRIVATE)
            public static class DefaultProject {
                public static final String V1 = PATH + "/before";
                public static final String V2 = PATH + "/after";

                public static String getPathToFile(String fileName) {
                    return FileUtilities.buildPath(V1, fileName);
                }
            }

            public static class Jira {
                public static final String DRONE_ISSUES = PATH + "/jira"
                    + "/drone_response.json";
            }
        }
    }
}
