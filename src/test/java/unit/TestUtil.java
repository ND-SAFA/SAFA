package unit;

import java.io.UnsupportedEncodingException;

import org.json.JSONException;
import org.json.JSONObject;
import org.springframework.test.web.servlet.MvcResult;

/**
 * Responsible for holding any response/request parsing functions.
 */
public class TestUtil {

    public static JSONObject asJson(MvcResult result) throws UnsupportedEncodingException, JSONException {
        String content = result.getResponse().getContentAsString();
        return content.equals("") ? new JSONObject() : new JSONObject(content);
    }
}
