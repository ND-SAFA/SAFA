package edu.nd.crc.safa.test.services;

import edu.nd.crc.safa.config.ObjectMapperConfig;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

public class MappingTestService {
    protected static ObjectMapper mapper = ObjectMapperConfig.create();

    public static <T> T toClass(String response, Class<T> targetClass) {
        try {
            return mapper.readValue(response, targetClass);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }
}
