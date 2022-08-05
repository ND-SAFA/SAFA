package edu.nd.crc.safa.authentication;

import java.io.IOException;
import java.util.ArrayList;
import javax.servlet.FilterChain;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import edu.nd.crc.safa.config.SecurityConstants;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.SneakyThrows;
import org.json.JSONObject;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

/**
 * Authenticates user when sending credentials to login route. If successful, generates and returns JWT token.
 */
public class AuthenticationFilter extends UsernamePasswordAuthenticationFilter {

    private final AuthenticationManager authenticationManager;
    private final TokenService tokenService;

    public AuthenticationFilter(AuthenticationManager authenticationManager,
                                TokenService tokenService) {
        super(authenticationManager);
        this.authenticationManager = authenticationManager;
        this.tokenService = tokenService;
    }

    /**
     * Attempts to parse payload as a SafaUser entity and look up this user. CORS headers is set manually
     *
     * @param req The request made to the server.
     * @param res The response object sent back to the client.
     * @return Authentication object signally a successful user authentication.
     * @throws AuthenticationException If given user is not found in database.
     */
    @SneakyThrows
    @Override
    public Authentication attemptAuthentication(HttpServletRequest req,
                                                HttpServletResponse res) throws AuthenticationException {
        SafaUser applicationUser = new ObjectMapper().readValue(req.getInputStream(), SafaUser.class);
        UsernamePasswordAuthenticationToken token = new UsernamePasswordAuthenticationToken(
            applicationUser.getEmail(),
            applicationUser.getPassword(),
            new ArrayList<>());

        return authenticationManager.authenticate(token);
    }

    /**
     * Creates a JSON response body containing authorization token.
     */
    @Override
    protected void successfulAuthentication(HttpServletRequest req,
                                            HttpServletResponse res,
                                            FilterChain chain,
                                            Authentication auth) throws IOException {

        String username = ((SafaUserDetails) auth.getPrincipal()).getUsername();
        String token = this.tokenService.createTokenForUsername(username, SecurityConstants.LOGIN_EXPIRATION_TIME);
        JSONObject responseJson = new JSONObject();

        responseJson.put(SecurityConstants.TOKEN_NAME, token);
        res.setContentType("application/json");
        res.setCharacterEncoding("UTF-8");
        res.getWriter().write(responseJson.toString());
    }
}
