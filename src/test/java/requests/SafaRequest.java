package requests;

import java.io.File;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.function.Function;
import javax.servlet.http.Cookie;

import edu.nd.crc.safa.utilities.JsonFileUtilities;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.json.JSONArray;
import org.json.JSONObject;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockHttpServletResponse;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.ResultMatcher;
import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.asyncDispatch;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * Responsible for sending request and parsing responses
 * to and from the SAFA back-end.
 */
public class SafaRequest extends RouteBuilder<SafaRequest> {
    private static MockMvc mockMvc;
    private static Cookie authorizationToken = null;

    public SafaRequest(String path) {
        super(path);
    }

    public static SafaRequest withRoute(String route) {
        return new SafaRequest(route);
    }

    public static void setMockMvc(MockMvc mockMvc) {
        SafaRequest.mockMvc = mockMvc;
    }

    public static Cookie getAuthorizationToken() {
        return authorizationToken;
    }

    public static void setAuthorizationToken(Cookie authorizationToken) {
        SafaRequest.authorizationToken = authorizationToken;
    }

    public static void assertTokenExists() {
        assert SafaRequest.authorizationToken != null;
    }

    public static void clearAuthorizationToken() {
        SafaRequest.authorizationToken = null;
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
        MockHttpServletRequestBuilder requestBuilder = get(this.buildEndpoint());
        return sendAuthenticatedRequest(requestBuilder,
            expectedResultMatcher,
            authorizationToken,
            ResponseParser::jsonCreator);
    }

    protected <T> T sendGet(Function<String, T> responseParser) throws Exception {
        return sendAuthenticatedRequest(get(this.buildEndpoint()),
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

    public JSONObject putWithJsonObject(Object body, ResultMatcher resultMatcher) throws Exception {
        return sendAuthenticatedRequest(
            put(this.buildEndpoint())
                .content(stringify(body))
                .contentType(MediaType.APPLICATION_JSON),
            resultMatcher,
            SafaRequest.authorizationToken,
            ResponseParser::jsonCreator
        );
    }

    public JSONObject putWithJsonObject(Object body) throws Exception {
        return putWithJsonObject(body, status().is2xxSuccessful());
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
                                         Cookie localAuthorizationToken
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
        return makeAsyncRequestWithoutBody(post(this.buildEndpoint()), resultMatcher);
    }

    public JSONObject putWithoutBody(ResultMatcher resultMatcher) throws Exception {
        return makeAsyncRequestWithoutBody(put(this.buildEndpoint()), resultMatcher);
    }

    public JSONObject getWithoutBody(ResultMatcher resultMatcher) throws Exception {
        return makeAsyncRequestWithoutBody(get(this.buildEndpoint()), resultMatcher);
    }

    public <T> T getWithResponseParser(Function<String, T> responseParser,
                                       ResultMatcher resultMatcher) throws Exception {
        return getWithResponseParser(
                responseParser,
                resultMatcher,
                SafaRequest.authorizationToken
        );
    }

    public <T> T getWithResponseParser(Function<String, T> responseParser) throws Exception {
        return getWithResponseParser(
                responseParser,
                status().is2xxSuccessful()
        );
    }

    public <T> T getAsType(TypeReference<T> typeReference) throws Exception {
        return getWithResponseParser(
                string -> this.jacksonParse(string, typeReference),
                status().is2xxSuccessful()
        );
    }

    private <T> T jacksonParse(String string, TypeReference<T> typeReference) {
        try {
            return new ObjectMapper().readValue(string, typeReference);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }

    private <T> T getWithResponseParser(Function<String, T> responseParser,
                                        ResultMatcher resultMatcher,
                                        Cookie localAuthorizationToken
    ) throws Exception {
        return sendAuthenticatedRequest(
                get(this.buildEndpoint()),
                resultMatcher,
                localAuthorizationToken,
                responseParser
        );
    }

    public JSONObject makeAsyncRequestWithoutBody(MockHttpServletRequestBuilder request,
                                                  ResultMatcher resultMatcher) throws Exception {

        if (authorizationToken != null) {
            request = request.cookie(authorizationToken);
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
                                             Cookie authorizationToken,
                                             Function<String, T> responseParser) throws Exception {
        if (authorizationToken != null) {
            request = request.cookie(authorizationToken);
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

    public Optional<Cookie> sendPostRequestAndRetrieveCookie(Object body,
                                                             ResultMatcher test,
                                                             String cookieName) throws Exception {
        MvcResult requestResult = mockMvc
            .perform(post(this.buildEndpoint())
                .content(stringify(body))
                .contentType(MediaType.APPLICATION_JSON))
            .andExpect(test)
            .andReturn();

        MockHttpServletResponse response = requestResult.getResponse();
        Cookie[] cookies = response.getCookies();

        if (cookies.length == 0) {
            return Optional.empty();
        }

        return Arrays.stream(response.getCookies())
            .filter(c -> c.getName().equals(cookieName))
            .findFirst();
    }
}
