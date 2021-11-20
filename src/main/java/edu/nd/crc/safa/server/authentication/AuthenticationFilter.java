package edu.nd.crc.safa.server.authentication;

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
import org.json.JSONObject;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

/**
 * Authenticates user when sending credentials to login route. If successful, generates and returns JWT token.
 */
public class AuthenticationFilter extends UsernamePasswordAuthenticationFilter {

    private final AuthenticationManager authenticationManager;
    private final SecurityConstants securityConstants;

    public AuthenticationFilter(AuthenticationManager authenticationManager, SecurityConstants securityConstants) {
        super(authenticationManager);
        this.authenticationManager = authenticationManager;
        this.securityConstants = securityConstants;
    }

    /**
     * Attempts to parse payload as a SafaUser entity and look up this user. CORS headers is set manually
     *
     * @param req The request made to the server.
     * @param res The response object sent back to the client.
     * @return Authentication object signally a successful user authentication.
     * @throws AuthenticationException If given user is not found in database.
     */
    @Override
    public Authentication attemptAuthentication(HttpServletRequest req,
                                                HttpServletResponse res) throws AuthenticationException {
        try {
            SafaUser applicationUser = new ObjectMapper().readValue(req.getInputStream(), SafaUser.class);
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
     * Creates a JSON response body containing authorization token.
     */
    @Override
    protected void successfulAuthentication(HttpServletRequest req,
                                            HttpServletResponse res,
                                            FilterChain chain,
                                            Authentication auth) throws IOException, ServletException {
        Date exp = new Date(System.currentTimeMillis() + SecurityConstants.EXPIRATION_TIME);
        Key key = Keys.hmacShaKeyFor(securityConstants.key.getBytes());
        Claims claims = Jwts.claims().setSubject(((User) auth.getPrincipal()).getUsername());
        String token = Jwts
            .builder()
            .setClaims(claims)
            .signWith(SignatureAlgorithm.HS512, key)
            .setExpiration(exp).compact();
        res.setContentType("application/json");
        res.setCharacterEncoding("UTF-8");
        JSONObject responseJson = new JSONObject();
        responseJson.put(SecurityConstants.TOKEN_NAME, token);
        res.getWriter().write(responseJson.toString());
    }
}
