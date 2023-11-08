package edu.nd.crc.safa.authentication;

import java.security.Key;
import java.util.Date;

import edu.nd.crc.safa.config.SecurityConstants;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * Responsible for creating and reading JWT tokens for application.
 */
@Service
@AllArgsConstructor
public class TokenService {

    private final SecurityConstants securityConstants;

    public String createTokenForUsername(String userName, long expirationDelta) {
        Date exp = new Date(System.currentTimeMillis() + expirationDelta);
        return createTokenForUsername(userName, exp);
    }

    public String createTokenForUsername(String userName, Date exp) {
        Key key = Keys.hmacShaKeyFor(securityConstants.getKey().getBytes());
        Claims claims = Jwts.claims().setSubject(userName);

        return Jwts
            .builder()
            .setClaims(claims)
            .signWith(key, SignatureAlgorithm.HS512)
            .setExpiration(exp)
            .compact();
    }

    public Claims getTokenClaims(String token) {
        return Jwts
            .parserBuilder()
            .setSigningKey(Keys.hmacShaKeyFor(securityConstants.getKey().getBytes()))
            .build()
            .parseClaimsJws(token)
            .getBody();
    }
}
