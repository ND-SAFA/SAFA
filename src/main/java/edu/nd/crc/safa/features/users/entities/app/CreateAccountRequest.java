package edu.nd.crc.safa.features.users.entities.app;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
@Data
public class CreateAccountRequest extends UserIdentifierDTO {
    /**
     * User password to create account with.
     */
    String password;
}
