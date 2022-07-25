package edu.nd.crc.safa.builders.requests;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;

import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.builders.MultipartRequestService;

import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.request.MockMultipartHttpServletRequestBuilder;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

public class SafaMultiPartRequest extends SafaRequest {
    public SafaMultiPartRequest(String path) {
        super(path);
    }

    public MockMultipartHttpServletRequestBuilder createMultiPartRequest(String routeName, String pathToFiles)
        throws IOException {
        String attributeName = "files";

        List<MockMultipartFile> files =
            MultipartRequestService.readDirectoryAsMockMultipartFiles(pathToFiles, attributeName);
        MockMultipartHttpServletRequestBuilder request = multipart(routeName);

        for (MockMultipartFile file : files) {
            request.file(file);
        }

        return request;
    }

    protected MockMultipartHttpServletRequestBuilder buildRequest() {
        return MockMvcRequestBuilders.multipart(this.buildEndpoint());
    }
}
