package edu.nd.crc.safa.features.users.entities.app;

import java.util.UUID;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Represents the application side view of an account.
 */
@NoArgsConstructor
@Data
public class UserIdentifierDTO {
    /**
     * Unique identifier for user.
     */
    @NotNull
    UUID userId;

    /**
     * User's email.
     */
    @NotNull
    @NotEmpty
    String email;

    public UserIdentifierDTO(SafaUser safaUser) {
        this.userId = safaUser.getUserId();
        this.email = safaUser.getEmail();
    }
}
