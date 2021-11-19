package edu.nd.crc.safa.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class SecurityConstants {
    public static final String HEADER_NAME = "Authorization";
    public static final Long EXPIRATION_TIME = 1000L * 60 * 30;

    @Value("${jwt.key}")
    public String key;
}
