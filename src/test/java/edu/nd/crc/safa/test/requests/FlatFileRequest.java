package edu.nd.crc.safa.test.requests;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.io.File;
import java.util.List;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.features.flatfiles.services.MultipartRequestService;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.json.JSONObject;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.ResultMatcher;

/**
 * A request containing one or more flat files.
 */
public class FlatFileRequest extends SafaMultiPartRequest {

    public FlatFileRequest(String path) {
        super(path);
    }

    /**
     * Updates project through flat files in given directory.
     *
     * @param projectVersion The project version to commit any changes to.
     * @param pathToFileDir  The directory containing the flat files defining the project.
     * @return Response of request
     * @throws Exception Throws exception is HTTP request fails.
     */
    public static JSONObject updateProjectVersionFromFlatFiles(
        ProjectVersion projectVersion,
        String pathToFileDir) throws Exception {
        JSONObject kwargs = new JSONObject();
        kwargs.put(ProjectVariables.AS_COMPLETE_SET, true);
        return SafaRequest
            .withRoute(AppRoutes.FlatFiles.UPDATE_PROJECT_VERSION_FROM_FLAT_FILES)
            .withVersion(projectVersion)
            .getFlatFileHelper()
            .postWithFilesInDirectory(pathToFileDir, kwargs);
    }

    /**
     * @param pathToFile Path to file to be attached to request.
     * @return Response to HTTP request.
     * @throws Exception Throws exception if server fails to send request.
     */
    public JSONObject postWithFile(String pathToFile) throws Exception {
        String attributeName = "file";
        MockMultipartFile file = MultipartRequestService.readAsMockMultipartFile(pathToFile, attributeName);
        return sendRequestWithFiles(List.of(file), status().is2xxSuccessful(), new JSONObject());
    }

    public JSONObject postWithFiles(List<File> files, JSONObject kwargs) throws Exception {
        List<MockMultipartFile> mockMultipartFiles = MultipartRequestService.convertToMockMultipartFiles(files,
            "files");
        return this.sendRequestWithFiles(mockMultipartFiles, status().is2xxSuccessful(), kwargs);
    }

    /**
     * Attaches files in directory to request and sends it.
     *
     * @param pathToFileDir Path to directory containing files attached to request.
     * @param kwargs        Variables parameters added to request.
     * @return Response to HTTP request.
     * @throws Exception Throws exception if error occurred during reading files or sending request.
     */
    public JSONObject postWithFilesInDirectory(String pathToFileDir, JSONObject kwargs) throws Exception {
        return postWithFilesInDirectory(pathToFileDir, status().is2xxSuccessful(), kwargs);
    }

    /**
     * Attaches files in directory to request and sends it. Uses result matcher to validate response.
     *
     * @param pathToFileDir Path to directory containing files attached to request.
     * @param resultMatcher Expected status of request.
     * @param kwargs        Parameters added to request
     * @return Response to HTTP request.
     * @throws Exception Throws exception if error occurred during reading files or sending request.
     */
    public JSONObject postWithFilesInDirectory(String pathToFileDir,
                                               ResultMatcher resultMatcher,
                                               JSONObject kwargs) throws Exception {
        SafaRequest.assertTokenExists();

        String attributeName = "files";

        List<MockMultipartFile> files =
            MultipartRequestService.readDirectoryAsMockMultipartFiles(pathToFileDir, attributeName);
        return sendRequestWithFiles(files, resultMatcher, kwargs);
    }
}
