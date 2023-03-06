package edu.nd.crc.safa.test.services;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

public class MappingTestService {
    protected static ObjectMapper mapper = new ObjectMapper();

    public static <T> T toClass(String response, Class<T> targetClass) throws JsonProcessingException {
        return mapper.readValue(response, targetClass);
    }
}
