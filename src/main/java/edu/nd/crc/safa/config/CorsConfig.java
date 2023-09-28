package edu.nd.crc.safa.config;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
import org.springframework.web.filter.CorsFilter;

@Configuration
public class CorsConfig {
    private static final List<String> allowedOrigins = Arrays.asList(
        "http://localhost:8080",
        "http://localhost:8081",
        "https://localhost:8080",
        "https://localhost:8081",
        "https://localhost.safa.ai:8080",
        "https://safa-fend-dev-5asg6qsnba-uc.a.run.app",
        "https://safa-fend-prod-5asg6qsnba-uc.a.run.app",
        "https://dev.safa.ai",
        "https://app.safa.ai",
        "https://dev-fend.safa.ai",
        "https://prod-fend.safa.ai"
    );

    private static final List<String> allowedMethods = Arrays.asList("GET", "POST", "PUT", "DELETE");

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration cors = new CorsConfiguration();

        cors.setAllowedOrigins(allowedOrigins);
        cors.setAllowedMethods(allowedMethods);
        cors.setAllowedHeaders(Collections.singletonList("*"));
        cors.setAllowCredentials(true);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", cors);

        return source;
    }

    @Bean
    public CorsFilter corsFilter() {
        return new CorsFilter(corsConfigurationSource());
    }
}
