package edu.nd.crc.safa.config;

import java.util.List;

import lombok.Getter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

/**
 * Container for JWT token secrets.
 */
@Component
public class SecurityConstants {
    public static final Long LOGIN_EXPIRATION_TIME = 1000L * 60 * 3000; // milliseconds until expiration
    public static final Long ACCOUNT_CONFIRMATION_EXPIRATION_TIME = 1000L * 60 * 3600;
    public static final Long FORGOT_PASSWORD_EXPIRATION_TIME = 1000L * 60 * 3000;
    public static final String JWT_COOKIE_NAME = "SAFA-TOKEN";
    public static final String COOKIE_NAME = "Cookie";
    public static final List<String> allowedCorsHeaders = List.of("X-Requested-With",
        "Origin", "Content-Type", "Accept",
        "Authorization", "Access-Control-Allow-Credentials", "Access-Control-Allow-Headers",
        "Access-Control-Allow-Methods", "Access-Control-Allow-Origin",
        "Access-Control-Expose-Headers", "Access-Control-Max-Age",
        "Access-Control-Request-Headers", "Access-Control-Request-Method", "Age", "Allow", "Alternates",
        "Content-Range", "Content-Disposition", "Content-Description");
    @Getter
    @Value("${jwt.key}")
    private String key;
}
