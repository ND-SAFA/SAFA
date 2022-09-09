package requests;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.asyncDispatch;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.io.File;
import java.util.List;
import java.util.function.Function;

import edu.nd.crc.safa.utilities.JsonFileUtilities;

import org.json.JSONArray;
import org.json.JSONObject;
import org.springframework.http.MediaType;
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
    private static String authorizationToken = "";

    public SafaRequest(String path) {
        super(path);
    }

    public static SafaRequest withRoute(String route) {
        return new SafaRequest(route);
    }

    public static void setMockMvc(MockMvc mockMvc) {
        SafaRequest.mockMvc = mockMvc;
    }

    public static String getAuthorizationToken() {
        return authorizationToken;
    }

    public static void setAuthorizationToken(String authorizationToken) {
        SafaRequest.authorizationToken = authorizationToken;
    }

    public static void assertTokenExists() {
        assert SafaRequest.authorizationToken != null && SafaRequest.authorizationToken.length() > 0;
    }

    public static void clearAuthorizationToken() {
        SafaRequest.authorizationToken = "";
    }

    public FlatFileRequest getFlatFileHelper() {
        return new FlatFileRequest(this.path);
    }

    public List<File> getWithFilesInZip() throws Exception {
        return sendGet(ResponseParser::zipFileParser);
    }

    public JSONArray getWithJsonArray() throws Exception {
        return sendGet(ResponseParser::arrayCreator);
    }

    public JSONObject getWithJsonObject() throws Exception {
        return sendGet(ResponseParser::jsonCreator);
    }

    public JSONObject getWithJsonObject(ResultMatcher expectedResultMatcher) throws Exception {
        MockHttpServletRequestBuilder requestBuilder = MockMvcRequestBuilders.get(this.buildEndpoint());
        return sendAuthenticatedRequest(requestBuilder,
            expectedResultMatcher,
            authorizationToken,
            ResponseParser::jsonCreator);
    }

    protected <T> T sendGet(Function<String, T> responseParser) throws Exception {
        return sendAuthenticatedRequest(MockMvcRequestBuilders.get(this.buildEndpoint()),
            status().isOk(),
            authorizationToken,
            responseParser);
    }

    public JSONArray postWithJsonArray(Object body) throws Exception {
        return postWithResponseParser(body, ResponseParser::arrayCreator);
    }

    public JSONObject postWithJsonObject(Object body) throws Exception {
        return postWithResponseParser(body, ResponseParser::jsonCreator);
    }

    public JSONObject postWithJsonObject(Object body, ResultMatcher resultMatcher) throws Exception {
        return postWithResponseParser(body, ResponseParser::jsonCreator, resultMatcher);
    }

    public <T> T postWithResponseParser(Object body,
                                        Function<String, T> responseParser,
                                        ResultMatcher resultMatcher) throws Exception {
        return postWithResponseParser(
            body,
            responseParser,
            resultMatcher,
            SafaRequest.authorizationToken
        );
    }

    private <T> T postWithResponseParser(Object body, Function<String, T> responseParser) throws Exception {
        return postWithResponseParser(
            body,
            responseParser,
            status().is2xxSuccessful());
    }

    private <T> T postWithResponseParser(Object body,
                                         Function<String, T> responseParser,
                                         ResultMatcher resultMatcher,
                                         String localAuthorizationToken
    ) throws Exception {
        return sendAuthenticatedRequest(
            post(this.buildEndpoint())
                .content(stringify(body))
                .contentType(MediaType.APPLICATION_JSON),
            resultMatcher,
            localAuthorizationToken,
            responseParser
        );
    }

    public JSONObject postWithoutBody(ResultMatcher resultMatcher) throws Exception {
        MockHttpServletRequestBuilder request = post(this.buildEndpoint());

        if (authorizationToken != null && !authorizationToken.equals("")) {
            request = request.header("Authorization", authorizationToken);
        }

        MvcResult result = mockMvc
            .perform(request)
            .andReturn();

        String response = mockMvc
            .perform(asyncDispatch(result))
            .andExpect(resultMatcher)
            .andReturn()
            .getResponse()
            .getContentAsString();

        return ResponseParser.jsonCreator(response);
    }

    private String stringify(Object body) {
        String content;
        if (body instanceof JSONObject || body instanceof JSONArray) {
            return body.toString();
        } else if (body instanceof List) {
            return JsonFileUtilities.toJsonArray(body).toString();
        } else {
            return JsonFileUtilities.toJson(body).toString();
        }
    }

    public JSONObject deleteWithJsonObject() throws Exception {
        return deleteWithJsonObject(status().is2xxSuccessful());
    }

    public JSONObject deleteWithJsonObject(ResultMatcher resultMatcher) throws Exception {
        return sendAuthenticatedRequest(MockMvcRequestBuilders.delete(this.buildEndpoint()),
            resultMatcher,
            authorizationToken,
            ResponseParser::jsonCreator);
    }

    protected <T> T sendAuthenticatedRequest(MockHttpServletRequestBuilder request,
                                             ResultMatcher test,
                                             String authorizationToken,
                                             Function<String, T> responseParser) throws Exception {
        if (authorizationToken != null && !authorizationToken.equals("")) {
            request = request.header("Authorization", authorizationToken);
        }
        return sendRequestAndParseResponse(request, test, responseParser);
    }

    protected <T> T sendRequestAndParseResponse(MockHttpServletRequestBuilder request,
                                                ResultMatcher test,
                                                Function<String, T> stringCreator) throws Exception {

        MvcResult requestResult = mockMvc
            .perform(request)
            .andExpect(test)
            .andReturn();

        MockHttpServletResponse response = requestResult.getResponse();
        String content = response.getContentAsString();
        return stringCreator.apply(content);
    }
}
