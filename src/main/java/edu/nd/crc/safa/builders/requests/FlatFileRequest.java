package edu.nd.crc.safa.builders.requests;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.List;

import edu.nd.crc.safa.builders.MultipartRequestService;
import edu.nd.crc.safa.builders.ResponseParser;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.json.JSONObject;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.ResultMatcher;
import org.springframework.test.web.servlet.request.MockMultipartHttpServletRequestBuilder;

/**
 * Represents a request to upload flat files to the server.
 */
public class FlatFileRequest extends SafaMultiPartRequest {

    public FlatFileRequest(String path) {
        super(path);
    }

    public static JSONObject updateProjectVersionFromFlatFiles(
        ProjectVersion projectVersion,
        String pathToFileDir) throws Exception {
        return SafaRequest
            .withRoute(AppRoutes.Projects.FlatFiles.updateProjectVersionFromFlatFiles)
            .withVersion(projectVersion)
            .getFlatFileHelper()
            .uploadFlatFilesToVersion(pathToFileDir);
    }

    public JSONObject uploadFlatFilesToVersion(String pathToFileDir) throws Exception {
        return uploadFlatFilesToVersion(pathToFileDir, status().is2xxSuccessful());
    }

    public JSONObject uploadSingleFile(String pathToFile)
        throws Exception {
        String attributeName = "file";

        MockMultipartFile file = MultipartRequestService.createFile(pathToFile, attributeName);
        return uploadFlatFilesToVersion(List.of(file), status().is2xxSuccessful());
    }

    public JSONObject uploadFlatFilesToVersion(String pathToFileDir, ResultMatcher resultMatcher) throws Exception {
        SafaRequest.assertTokenExists();

        String attributeName = "files";

        List<MockMultipartFile> files =
            MultipartRequestService.createMockMultipartFilesFromDirectory(pathToFileDir, attributeName);
        return uploadFlatFilesToVersion(files, resultMatcher);
    }

    public JSONObject uploadFlatFilesToVersion(List<MockMultipartFile> files,
                                               ResultMatcher resultMatcher
    ) throws Exception {
        SafaRequest.assertTokenExists();
        MockMultipartHttpServletRequestBuilder request = this.buildRequest();

        for (MockMultipartFile file : files) {
            request.file(file);
        }

        return sendAuthenticatedRequest(
            request,
            resultMatcher,
            SafaRequest.getAuthorizationToken(),
            ResponseParser::jsonCreator
        );
    }
}
