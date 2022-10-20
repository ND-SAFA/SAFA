package edu.nd.crc.safa.authentication;

import edu.nd.crc.safa.features.common.ServiceProvider;

import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;

/**
 * Wrapper class for setting thes session authorization.
 */
public interface AuthorizationSetter {
    /**
     * Sets the current session authorization to user found with given email.
     *
     * @param userEmail       Email of the user to set to current session.
     * @param serviceProvider Provides persistent services.
     */
    static void setSessionAuthorization(String userEmail, ServiceProvider serviceProvider) {
        UserDetails userDetails = serviceProvider.getUserDetailsService().loadUserByUsername(userEmail);
        UsernamePasswordAuthenticationToken authorization = new UsernamePasswordAuthenticationToken(
            userDetails,
            null,
            userDetails.getAuthorities());

        SecurityContextHolder.getContext().setAuthentication(authorization);
    }
}
