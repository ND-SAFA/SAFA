package unit;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.UnsupportedEncodingException;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.json.JSONException;
import org.json.JSONObject;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.MvcResult;

/**
 * Responsible for holding any response/request parsing functions.
 */
public class TestUtil {

    public static JSONObject asJson(MvcResult result) throws UnsupportedEncodingException, JSONException {
        return new JSONObject(result.getResponse().getContentAsString());
    }

    public static String asJsonString(final Object obj) {
        try {
            return new ObjectMapper().writeValueAsString(obj);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    public static MockMultipartFile createMultipartFile(String path, String name) throws FileNotFoundException,
        IOException {
        return new MockMultipartFile(name, new FileInputStream(new File(path)));
    }

    public static MockMultipartFile createMultipartFile(String path) throws FileNotFoundException,
        IOException {
        return new MockMultipartFile("files", new FileInputStream(new File(path)));
    }
}
