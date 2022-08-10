package edu.nd.crc.safa.builders.requests;

import java.util.List;

import edu.nd.crc.safa.builders.ResponseParser;

import org.json.JSONObject;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.ResultMatcher;
import org.springframework.test.web.servlet.request.MockMultipartHttpServletRequestBuilder;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

/**
 * Defines generic multi-part request containing a series of files.
 */
public abstract class SafaMultiPartRequest extends SafaRequest {
    protected SafaMultiPartRequest(String path) {
        super(path);
    }

    /**
     * Creates the multi-part request with given files attached.
     *
     * @param files         The files attached to multipart request.
     * @param resultMatcher The expected status of the HTTP request.
     * @param kwargs        Set of parameters added to request.
     * @return Response to HTTP request.
     * @throws Exception Throws exception if server fails to send HTTP request.
     */
    protected JSONObject sendRequestWithFiles(List<MockMultipartFile> files,
                                              ResultMatcher resultMatcher,
                                              JSONObject kwargs
    ) throws Exception {
        SafaRequest.assertTokenExists();
        MockMultipartHttpServletRequestBuilder request = this.buildMultiPartRequest();

        // Step - Adding file to request
        for (MockMultipartFile file : files) {
            request.file(file);
        }

        // Step - Adding external parameters to request
        for (String key : kwargs.keySet()) {
            byte[] content = kwargs.get(key).toString().getBytes();
            MockMultipartFile jsonFile = new MockMultipartFile(key, "", "application/json", content);
            request.file(jsonFile);
        }

        // Step - Send request
        return sendAuthenticatedRequest(
            request,
            resultMatcher,
            SafaRequest.getAuthorizationToken(),
            ResponseParser::jsonCreator
        );
    }

    /**
     * Creates MultiPart request with current set endpoint.
     *
     * @return MultiPart request
     */
    protected MockMultipartHttpServletRequestBuilder buildMultiPartRequest() {
        return MockMvcRequestBuilders.multipart(this.buildEndpoint());
    }
}
