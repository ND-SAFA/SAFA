package edu.nd.crc.safa.config;

import java.util.Arrays;
import java.util.List;

import edu.nd.crc.safa.authentication.AuthenticationFilter;
import edu.nd.crc.safa.authentication.AuthorizationFilter;
import edu.nd.crc.safa.authentication.AuthorizationService;
import edu.nd.crc.safa.authentication.TokenService;

import lombok.AllArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

/**
 * Creates the authentication solution for our app including:
 * 1. Create CORS policy allowing localhost host, dev, and production applications.
 * 2. Disabled Cross Site Request Forgery policy (TODO: Replace with some policy).
 * 3. Enabled app-wide authentication except for login and create account routes. TODO: Add forgot password route.
 */
@AllArgsConstructor
@Configuration
@EnableWebSecurity
public class AuthenticationConfig {
    public static final List<String> OPEN_ENDPOINTS = List.of(AppRoutes.Accounts.LOGIN,
        AppRoutes.Accounts.CREATE_ACCOUNT,
        AppRoutes.Accounts.FORGOT_PASSWORD,
        AppRoutes.Accounts.RESET_PASSWORD);

    private final AuthorizationService authorizationService;
    private final TokenService tokenService;
    private final UserDetailsService userDetailsService;

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http,
                                                   AuthenticationManager authenticationManager)
        throws Exception {
        http
            .cors(Customizer.withDefaults())
            .csrf(AbstractHttpConfigurer::disable)
            .authorizeHttpRequests(requests -> requests
                .requestMatchers(
                    AppRoutes.Accounts.LOGIN,
                    AppRoutes.Accounts.CREATE_ACCOUNT,
                    AppRoutes.Accounts.FORGOT_PASSWORD,
                    AppRoutes.Accounts.RESET_PASSWORD,
                    "/websocket/**",
                    "/swagger-ui/**", // Needed to get config
                    "/v3/api-docs/**",
                    "/docs/**")
                .permitAll()
                .anyRequest()
                .authenticated())
            // Authentication Filters
            .addFilter(new AuthenticationFilter(authenticationManager, tokenService))
            .addFilter(new AuthorizationFilter(authenticationManager, authorizationService))
            .sessionManagement((sessionManager) -> sessionManager
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS));
        return http.build();
    }

    @Bean
    public DaoAuthenticationProvider authProvider() {
        DaoAuthenticationProvider authProvider = new DaoAuthenticationProvider();
        authProvider.setUserDetailsService(userDetailsService);
        authProvider.setPasswordEncoder(passwordEncoder());
        return authProvider;
    }

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration config = new CorsConfiguration();

        config.setAllowCredentials(true);
        config.addAllowedOriginPattern("https://localhost.safa.ai:8080");
        config.addAllowedOriginPattern("http://localhost:8080");
        config.setAllowedHeaders(Arrays.asList("X-Requested-With", "Origin", "Content-Type", "Accept",
            "Authorization", "Access-Control-Allow-Credentials", "Access-Control-Allow-Headers", "Access-Control-Allow-Methods",
            "Access-Control-Allow-Origin", "Access-Control-Expose-Headers", "Access-Control-Max-Age",
            "Access-Control-Request-Headers", "Access-Control-Request-Method", "Age", "Allow", "Alternates",
            "Content-Range", "Content-Disposition", "Content-Description"));
        config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"));
        config.setExposedHeaders(List.of(
            "Access-Control-Allow-Origin",
            "Access-Control-Allow-Methods",
            "Access-Control-Allow-Headers",
            "Access-Control-Allow-Credentials",
            "Access-Control-Max-Age"
        ));
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("*", config);
        source.registerCorsConfiguration("/**", config);
        return source;
    }

    @Bean
    public SecurityConstants getSecurityConstants() {
        return new SecurityConstants();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
