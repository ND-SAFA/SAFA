package edu.nd.crc.safa.server.entities.app;

import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.SafaUser;

/**
 * Represents the application side view of an account.
 */
public class UserAppEntity {

    UUID userId;
    String email;

    public UserAppEntity(SafaUser safaUser) {
        this.userId = safaUser.getUserId();
        this.email = safaUser.getEmail();
    }

    public UUID getUserId() {
        return userId;
    }

    public void setUserId(UUID userId) {
        this.userId = userId;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }
}
