package edu.nd.crc.safa.config;

import java.util.Arrays;
import java.util.List;
import javax.annotation.Resource;

import edu.nd.crc.safa.server.authentication.AuthenticationFilter;
import edu.nd.crc.safa.server.authentication.AuthorizationFilter;
import edu.nd.crc.safa.server.authentication.SafaUserService;
import edu.nd.crc.safa.server.authentication.TokenService;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.cors.CorsConfiguration;


/**
 * Creates the authentication solution for our app including:
 * 1. Create CORS policy allowing localhost host, dev, and production applications.
 * 2. Disabled Cross Site Request Forgery policy (TODO: Replace with some policy).
 * 3. Enabled app-wide authentication except for login and create account routes. TODO: Add forgot password route.
 */
@Configuration
@EnableWebSecurity
public class AuthenticationConfig extends WebSecurityConfigurerAdapter {

    private final List<String> allowedOrigins = Arrays.asList(
        "http://localhost:8080",
        "http://localhost:8081",
        "https://safa-fend-dev-5asg6qsnba-uc.a.run.app",
        "https://safa-fend-prod-5asg6qsnba-uc.a.run.app"
    );

    private final List<String> allowedMethods = Arrays.asList("GET", "POST", "PUT", "DELETE");

    @Resource
    private SafaUserService userDetailsService;

    @Resource
    private TokenService tokenService;

    @Override
    protected void configure(AuthenticationManagerBuilder auth) {
        auth.authenticationProvider(authProvider());
    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            // CORS
            .cors().configurationSource(request -> {
                var cors = new CorsConfiguration();
                cors.setAllowedOrigins(allowedOrigins);
                cors.setAllowedMethods(allowedMethods);
                cors.setAllowedHeaders(List.of("*"));
                cors.setAllowCredentials(true);
                return cors;
            }).and()
            .csrf().disable()
            // Endpoint Settings
            .authorizeRequests()
            .antMatchers(
                AppRoutes.loginLink,
                AppRoutes.createAccountLink,
                "/websocket/**").permitAll()
            .anyRequest().authenticated()
            // Authentication Filters
            .and()
            .addFilter(new AuthenticationFilter(authenticationManager(), tokenService))
            .addFilter(new AuthorizationFilter(authenticationManager(), tokenService))
            .sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS);
    }

    @Bean
    public DaoAuthenticationProvider authProvider() {
        DaoAuthenticationProvider authProvider = new DaoAuthenticationProvider();
        authProvider.setUserDetailsService(userDetailsService);
        authProvider.setPasswordEncoder(passwordEncoder());
        return authProvider;
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
