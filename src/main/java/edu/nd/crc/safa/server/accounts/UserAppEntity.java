package edu.nd.crc.safa.server.accounts;

import java.util.UUID;

import lombok.Data;

/**
 * Represents the application side view of an account.
 */
@Data
public class UserAppEntity {

    UUID userId;
    String email;

    public UserAppEntity(SafaUser safaUser) {
        this.userId = safaUser.getUserId();
        this.email = safaUser.getEmail();
    }
}
