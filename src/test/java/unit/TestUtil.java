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
        MockHttpServletResponse response = apiResponse.getResponse();
        String content = response.getContentAsString();
        return content.equals("") ? new JSONObject() : new JSONObject(content);
    }
}
