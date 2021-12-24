package edu.nd.crc.safa.server.authentication;

import java.security.Key;
import java.util.Date;
import javax.annotation.Resource;

import edu.nd.crc.safa.config.SecurityConstants;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;
import org.springframework.stereotype.Service;

/**
 * Responsible for creating and reading JWT tokens for application.
 */
@Service
public class TokenService {

    @Resource
    private final SecurityConstants securityConstants;

    public TokenService(SecurityConstants securityConstants) {
        this.securityConstants = securityConstants;
    }

    public String createTokenForUsername(String userName, long expirationDelta) {
        Date exp = new Date(System.currentTimeMillis() + expirationDelta);
        Key key = Keys.hmacShaKeyFor(securityConstants.key.getBytes());
        Claims claims = Jwts.claims().setSubject(userName);
        return Jwts
            .builder()
            .setClaims(claims)
            .signWith(SignatureAlgorithm.HS512, key)
            .setExpiration(exp).compact();
    }

    public Claims getTokenClaims(String token) {
        //TODO: replace these deprecated methods
        return Jwts
            .parser()
            .setSigningKey(Keys.hmacShaKeyFor(securityConstants.key.getBytes()))
            .parseClaimsJws(token)
            .getBody();
    }
}
