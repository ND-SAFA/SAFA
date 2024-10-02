package edu.nd.crc.safa.config;

import java.util.List;

import edu.nd.crc.safa.authentication.AuthenticationFilter;
import edu.nd.crc.safa.authentication.AuthorizationFilter;
import edu.nd.crc.safa.authentication.AuthorizationService;
import edu.nd.crc.safa.authentication.TokenService;

import jakarta.servlet.DispatcherType;
import lombok.AllArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpStatus;
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
import org.springframework.security.web.authentication.HttpStatusEntryPoint;
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
    public static final List<String> OPEN_ENDPOINTS = List.of(
        AppRoutes.Accounts.LOGIN,
        AppRoutes.Accounts.CREATE_ACCOUNT,
        AppRoutes.Accounts.FORGOT_PASSWORD,
        AppRoutes.Accounts.RESET_PASSWORD,
        AppRoutes.Stripe.WEBHOOK,
        "/swagger-ui/**",
        "/v3/api-docs/**",
        "/docs/**"
    );

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
                .requestMatchers(OPEN_ENDPOINTS.toArray(new String[0]))
                .permitAll()
                .dispatcherTypeMatchers(DispatcherType.ASYNC).permitAll()
                .anyRequest()
                .authenticated())
            // Authentication Filters
            .addFilter(new AuthenticationFilter(authenticationManager, tokenService))
            .addFilter(new AuthorizationFilter(authenticationManager, authorizationService))
            .sessionManagement((sessionManager) -> sessionManager
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .exceptionHandling(h -> h.authenticationEntryPoint(new HttpStatusEntryPoint(HttpStatus.UNAUTHORIZED)));
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
        config.addAllowedOriginPattern("http://localhost:8080");
        config.addAllowedOriginPattern("https://staging.safa.ai");
        config.addAllowedOriginPattern("https://app.safa.ai");
        config.addAllowedOriginPattern("https://dev.safa.ai");
        config.setAllowedHeaders(SecurityConstants.allowedCorsHeaders);
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
