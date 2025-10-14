package edu.nd.crc.safa.config;

import java.util.HashMap;
import java.util.Map;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.context.annotation.Configuration;

/**
 * Constructs the general object mapper for entire application
 */
@Configuration
public class ObjectMapperConfig {
    public static String serialize(Map<String, JsonNode> attributes) {
        try {
            return ObjectMapperConfig.create().writeValueAsString(attributes);
        } catch (JsonProcessingException e) {
            e.printStackTrace();
            return "{}";  // Return empty JSON on failure
        }
    }

    public static Map<String, JsonNode> deserialize(String jsonStr) {
        try {
            if (jsonStr == null || jsonStr.isEmpty()) {
                return new HashMap<>();
            }
            ObjectMapper objectMapper = ObjectMapperConfig.create();
            return objectMapper.readValue(jsonStr,
                objectMapper.getTypeFactory().constructMapType(Map.class, String.class, JsonNode.class));
        } catch (JsonProcessingException e) {
            e.printStackTrace();
            return new HashMap<>();  // Return empty map on failure
        }
    }

    /**
     * Creates a new object mapper with proper configuration.
     *
     * @return Object mapper object.
     */
    public static ObjectMapper create() {
        ObjectMapper mapper = new ObjectMapper();
        mapper.findAndRegisterModules();
        return mapper;
    }

    /**
     * @return Returns new object mapper.
     */
    public ObjectMapper getObjectMapper() {
        return create();
    }
}
