package edu.nd.crc.safa.config;

import javax.annotation.Resource;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import edu.nd.crc.safa.server.authentication.AuthenticationFilter;
import edu.nd.crc.safa.server.authentication.AuthorizationFilter;
import edu.nd.crc.safa.server.services.SafaUserService;

import org.apache.http.HttpStatus;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

@Configuration
@EnableWebSecurity
public class AuthenticationConfig extends WebSecurityConfigurerAdapter {

    @Resource
    private SafaUserService userDetailsService;

    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
        auth.authenticationProvider(authProvider());
    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .addFilter(new AuthenticationFilter(authenticationManager()))
            .addFilter(new AuthorizationFilter(authenticationManager()))
            .sessionManagement()
            .sessionCreationPolicy(SessionCreationPolicy.ALWAYS)
            .and()
            .csrf().disable()
            .formLogin()
            .usernameParameter("email")
            .loginProcessingUrl("/login/**")
            .failureHandler((HttpServletRequest request,
                             HttpServletResponse response,
                             AuthenticationException exception) -> {
                response.setStatus(HttpStatus.SC_UNAUTHORIZED);
            })
            .successHandler((HttpServletRequest request,
                             HttpServletResponse response,
                             Authentication authentication) -> {
                response.setStatus(HttpStatus.SC_OK);
            })
            .permitAll()
            .and()
            .authorizeRequests()
            .antMatchers("/login", "/sign-up")
            .permitAll()
            .anyRequest()
            .authenticated();

    }

    @Bean
    public DaoAuthenticationProvider authProvider() {
        DaoAuthenticationProvider authProvider = new DaoAuthenticationProvider();
        authProvider.setUserDetailsService(userDetailsService);
        authProvider.setPasswordEncoder(passwordEncoder());
        return authProvider;
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
