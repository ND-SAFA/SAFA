package edu.nd.crc.safa.server.authentication;

import static edu.nd.crc.safa.config.SecurityConstants.KEY;

import java.io.IOException;
import java.security.Key;
import java.util.ArrayList;
import java.util.Date;
import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import edu.nd.crc.safa.config.SecurityConstants;
import edu.nd.crc.safa.server.entities.db.SafaUser;

import com.fasterxml.jackson.databind.ObjectMapper;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

/**
 * Generates a token that is sent in the headers when the login is correct.
 */
public class AuthenticationFilter extends UsernamePasswordAuthenticationFilter {
    private final AuthenticationManager authenticationManager;

    public AuthenticationFilter(AuthenticationManager authenticationManager) {
        this.authenticationManager = authenticationManager;
    }

    @Override
    public Authentication attemptAuthentication(HttpServletRequest req,
                                                HttpServletResponse res) throws AuthenticationException {
        try {
            SafaUser applicationUser = new ObjectMapper().readValue(req.getInputStream(), SafaUser.class);
            System.out.println("USER:" + applicationUser);
            UsernamePasswordAuthenticationToken token = new UsernamePasswordAuthenticationToken(
                applicationUser.getEmail(),
                applicationUser.getPassword(),
                new ArrayList<>());
            return authenticationManager.authenticate(token);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }


    /**
     * Attaches a JWT token to response object when user is successfully authenticated. Token consists of the account
     * username as claim with new expiration date.
     */
    @Override
    protected void successfulAuthentication(HttpServletRequest req,
                                            HttpServletResponse res,
                                            FilterChain chain,
                                            Authentication auth) throws IOException, ServletException {
        Date exp = new Date(System.currentTimeMillis() + SecurityConstants.EXPIRATION_TIME);
        Key key = Keys.hmacShaKeyFor(KEY.getBytes());
        Claims claims = Jwts.claims().setSubject(((User) auth.getPrincipal()).getUsername());
        String token = Jwts
            .builder()
            .setClaims(claims)
            .signWith(SignatureAlgorithm.HS512, key)
            .setExpiration(exp).compact();
        res.addHeader("token", token);
    }
}
