package edu.nd.crc.safa.features.users.entities.app;

import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class PasswordForgottenRequest {

    /**
     * User's email
     */
    @NotNull
    @NotEmpty
    private String email;
}
