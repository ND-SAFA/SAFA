package edu.nd.crc.safa.config;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.context.annotation.Configuration;

/**
 * Constructs the general object mapper for entire application
 */
@Configuration
public class ObjectMapperConfig {
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
