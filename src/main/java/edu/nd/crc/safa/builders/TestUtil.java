package edu.nd.crc.safa.builders;

import java.io.UnsupportedEncodingException;

import edu.nd.crc.safa.server.entities.api.StringCreator;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.springframework.mock.web.MockHttpServletResponse;
import org.springframework.stereotype.Service;
import org.springframework.test.web.servlet.MvcResult;

/**
 * Responsible for holding any response/request parsing functions.
 */
@Service
public class TestUtil {
    public JSONObject apiResponseAsJsonObject(MvcResult apiResponse) throws UnsupportedEncodingException,
        JSONException {
        StringCreator<JSONObject> jsonCreator = (content) -> content.equals("") ?
            new JSONObject() : new JSONObject(content);
        return this.apiResponseAsJsonObject(apiResponse, jsonCreator);
    }

    public JSONArray apiResponseAsJsonArray(MvcResult apiResponse) throws UnsupportedEncodingException,
        JSONException {
        StringCreator<JSONArray> jsonCreator = (content) -> content.equals("") ?
            new JSONArray() : new JSONArray(content);
        return this.apiResponseAsJsonObject(apiResponse, jsonCreator);

    }

    public <T> T apiResponseAsJsonObject(
        MvcResult apiResponse,
        StringCreator<T> stringCreator) throws UnsupportedEncodingException,
        JSONException {
        MockHttpServletResponse response = apiResponse.getResponse();
        String content = response.getContentAsString();
        return stringCreator.create(content);
    }
}
