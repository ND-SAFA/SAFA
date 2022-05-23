package edu.nd.crc.safa.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

/**
 * Container for JWT token secrets.
 */
@Component
public class SecurityConstants {
    public static final String TOKEN_NAME = "token";
    public static final String AUTHORIZATION_HEADER = "Authorization";
    public static final Long LOGIN_EXPIRATION_TIME = 1000L * 60 * 3000; // milliseconds until expiration
    public static final Long ACCOUNT_CONFIRMATION_EXPIRATION_TIME = 1000L * 60 * 3600;
    @Value("${jwt.key}")
    public String key;
}
