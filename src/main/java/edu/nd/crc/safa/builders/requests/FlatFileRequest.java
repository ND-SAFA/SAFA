package edu.nd.crc.safa.builders.requests;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.List;

import edu.nd.crc.safa.builders.MultipartRequestService;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

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
        return SafaRequest
            .withRoute(AppRoutes.Projects.FlatFiles.updateProjectVersionFromFlatFiles)
            .withVersion(projectVersion)
            .getFlatFileHelper()
            .sendRequestWithFilesInDirectory(pathToFileDir);
    }

    /**
     * @param pathToFile Path to file to be attached to request.
     * @return Response to HTTP request.
     * @throws Exception Throws exception if server fails to send request.
     */
    public JSONObject sendRequestWithFile(String pathToFile) throws Exception {
        String attributeName = "file";
        MockMultipartFile file = MultipartRequestService.readAsMockMultipartFile(pathToFile, attributeName);
        return sendRequestWithFiles(List.of(file), status().is2xxSuccessful());
    }

    /**
     * Attaches files in directory to request and sends it.
     *
     * @param pathToFileDir Path to directory containing files attached to request.
     * @return Response to HTTP request.
     * @throws Exception Throws exception if error occurred during reading files or sending request.
     */
    public JSONObject sendRequestWithFilesInDirectory(String pathToFileDir) throws Exception {
        return sendRequestWithFilesInDirectory(pathToFileDir, status().is2xxSuccessful());
    }

    /**
     * Attaches files in directory to request and sends it. Uses result matcher to validate response.
     *
     * @param pathToFileDir Path to directory containing files attached to request.
     * @param resultMatcher Expected status of request.
     * @return Response to HTTP request.
     * @throws Exception Throws exception if error occurred during reading files or sending request.
     */
    public JSONObject sendRequestWithFilesInDirectory(String pathToFileDir,
                                                      ResultMatcher resultMatcher) throws Exception {
        SafaRequest.assertTokenExists();

        String attributeName = "files";

        List<MockMultipartFile> files =
            MultipartRequestService.readDirectoryAsMockMultipartFiles(pathToFileDir, attributeName);
        return sendRequestWithFiles(files, resultMatcher);
    }
}
