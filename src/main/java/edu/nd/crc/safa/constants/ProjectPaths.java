package edu.nd.crc.safa.constants;

import java.nio.file.Paths;
import java.util.Arrays;

import edu.nd.crc.safa.entities.Project;

/**
 * Contains common full paths used through app.
 */
public class ProjectPaths {
    public static final String PATH_TO_ROOT = System.getProperty("user.dir");
    public static final String PATH_TO_BUILD = PATH_TO_ROOT + "/build";
    public static final String PATH_TO_FLAT_FILES = PATH_TO_BUILD + "/uploadedFlatFiles";
    public static final String PATH_TO_GENERATED_DIR = PATH_TO_BUILD + "/generatedFiles";
    public static final String PATH_TO_TEST_RESOURCES = PATH_TO_ROOT + "/resources";


    private static String pathHelper(String... paths) {
        return Paths.get(Arrays.toString(paths)).toString();
    }

    public static String getPathToStorage(Project project) {
        return pathHelper(ProjectPaths.PATH_TO_FLAT_FILES, project.getProjectId().toString());
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
