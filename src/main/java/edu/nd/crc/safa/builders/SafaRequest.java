package edu.nd.crc.safa.builders;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.function.Function;

import org.json.JSONException;
import org.json.JSONObject;
import org.springframework.mock.web.MockHttpServletResponse;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.ResultMatcher;
import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

/**
 * Responsible for sending request and parsing responses
 * to and from the SAFA back-end.
 */
public class SafaRequest extends RouteBuilder<SafaRequest> {
    private static MockMvc mockMvc;
    private static String authorizationToken;

    public SafaRequest(String path) {
        super(path);
    }

    public static void setMockMvc(MockMvc mockMvc) {
        SafaRequest.mockMvc = mockMvc;
    }

    public static void setAuthorizationToken(String authorizationToken) {
        SafaRequest.authorizationToken = authorizationToken;
    }

    public List<File> getFilesInZipResponse() throws Exception {
        return sendGet(ResponseParser::zipFileParser);
    }

    public JSONObject getJSONResponse() throws Exception {
        return sendGet(ResponseParser::jsonCreator);
    }

    public <T> T sendGet(Function<String, T> responseParser) throws Exception {
        return sendRequestWithCreator(MockMvcRequestBuilders.get(this.buildEndpoint()),
            status().isOk(),
            authorizationToken,
            responseParser);
    }

    public <T> T sendRequestWithCreator(MockHttpServletRequestBuilder request,
                                        ResultMatcher test,
                                        String authorizationToken,
                                        Function<String, T> responseParser) throws Exception {
        if (!authorizationToken.equals("")) {
            request = request.header("Authorization", authorizationToken);
        }
        return sendRequestWithResponse(request, test, responseParser);
    }

    public <T> T sendRequestWithResponse(MockHttpServletRequestBuilder request,
                                         ResultMatcher test,
                                         Function<String, T> stringCreator) throws Exception {

        MvcResult response = mockMvc
            .perform(request)
            .andExpect(test)
            .andReturn();

        return this.apiResponseAsJsonObject(response, stringCreator);
    }

    public <T> T apiResponseAsJsonObject(
        MvcResult apiResponse,
        Function<String, T> stringCreator) throws IOException,
        JSONException {
        MockHttpServletResponse response = apiResponse.getResponse();
        String content = response.getContentAsString();
        return stringCreator.apply(content);
    }
}
