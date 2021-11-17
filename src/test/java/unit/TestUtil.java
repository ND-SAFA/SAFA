package unit;

import java.io.UnsupportedEncodingException;

import org.json.JSONException;
import org.json.JSONObject;
import org.springframework.mock.web.MockHttpServletResponse;
import org.springframework.test.web.servlet.MvcResult;

/**
 * Responsible for holding any response/request parsing functions.
 */
public class TestUtil {

    public static JSONObject apiResponseAsJson(MvcResult apiResponse) throws UnsupportedEncodingException,
        JSONException {
        return apiResponseAsJson(apiResponse, new String[]{});
    }

    public static JSONObject apiResponseAsJson(MvcResult apiResponse, String[] includeHeaders) throws UnsupportedEncodingException,
        JSONException {
        MockHttpServletResponse response = apiResponse.getResponse();
        String content = response.getContentAsString();
        JSONObject responseJson = content.equals("") ? new JSONObject() : new JSONObject(content);
        for (String headerName : includeHeaders) {
            responseJson.put(headerName, response.getHeader(headerName));
        }
        return responseJson;
    }
}
