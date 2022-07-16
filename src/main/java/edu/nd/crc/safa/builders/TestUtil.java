package edu.nd.crc.safa.builders;

import java.io.IOException;

import edu.nd.crc.safa.server.entities.api.StringCreator;

import org.json.JSONException;
import org.springframework.mock.web.MockHttpServletResponse;
import org.springframework.stereotype.Service;
import org.springframework.test.web.servlet.MvcResult;

/**
 * Responsible for holding any response/request parsing functions.
 */
@Service
public class TestUtil {
    public <T> T apiResponseAsJsonObject(
        MvcResult apiResponse,
        StringCreator<T> stringCreator) throws IOException,
        JSONException {
        MockHttpServletResponse response = apiResponse.getResponse();
        String content = response.getContentAsString();
        return stringCreator.create(content);
    }
}
