package edu.nd.crc.safa.constants;

import edu.nd.crc.safa.database.entities.Project;

/**
 * Contains common full paths used through app.
 */
public class ProjectPaths {
    public static final String PATH_TO_ROOT = System.getProperty("user.dir");
    public static final String PATH_TO_BUILD = PATH_TO_ROOT + "/build";
    public static final String PATH_TO_FLAT_FILES = PATH_TO_BUILD + "/uploadedFlatFiles";
    public static final String PATH_TO_GENERATED_DIR = PATH_TO_BUILD + "/generatedFiles";
    public static final String PATH_TO_TEST_RESOURCES = PATH_TO_ROOT + "/resources";

    public static String getPathToProjectFlatFiles(Project project) {
        return ProjectPaths.PATH_TO_FLAT_FILES + "/" + project.getProjectId().toString() + "/";
    }

    public static String getPathToProjectFlatFile(Project project, String fileName) {
        return getPathToProjectFlatFiles(project) + "/" + fileName;
    }
}
