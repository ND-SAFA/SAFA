package edu.nd.crc.safa.features.users.controllers;

import edu.nd.crc.safa.authentication.SafaUserService;
import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.app.UserAppEntity;
import edu.nd.crc.safa.features.users.entities.app.UserPassword;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.repositories.SafaUserRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/**
 * Controller containing endpoints for:
 * 1. Creating a new account
 * 2. Resetting user password (TODO)
 * 3. Confirming user account (TODO)
 * Note, logging into system is handled by spring boot default configuration at /login.
 */
@RestController
public class SafaUserController extends BaseController {

    private final SafaUserService safaUserService;
    private final SafaUserRepository safaUserRepository;
    private final PasswordEncoder passwordEncoder;

    @Autowired
    public SafaUserController(ResourceBuilder resourceBuilder,
                              SafaUserRepository safaUserRepository,
                              PasswordEncoder passwordEncoder,
                              SafaUserService safaUserService) {
        super(resourceBuilder);
        this.safaUserRepository = safaUserRepository;
        this.passwordEncoder = passwordEncoder;
        this.safaUserService = safaUserService;
    }

    /**
     * Creates new account with given email and password.
     * Error is thrown is email is already associated with another account.
     *
     * @param newUser User to create containing email and password.
     * @return Created user entity
     */
    @PostMapping(AppRoutes.Accounts.CREATE_ACCOUNT)
    public UserAppEntity createNewUser(@RequestBody SafaUser newUser) {
        String encodedPassword = this.passwordEncoder.encode(newUser.getPassword());
        SafaUser safaUser = new SafaUser(null,
            newUser.getEmail(),
            encodedPassword);
        this.safaUserRepository.save(safaUser);
        return new UserAppEntity(safaUser);
    }

    /**
     * Deletes account of authenticated user after confirming that given
     * password matches that of database.
     *
     * @param userPassword Authenticated user's password.
     */
    @PostMapping(AppRoutes.Accounts.DELETE_ACCOUNT)
    public void deleteAccount(@RequestBody UserPassword userPassword) {
        String confirmationPassword = userPassword.getPassword();
        if (confirmationPassword == null) {
            throw new SafaError("Received empty confirmation password.");
        }
        this.safaUserService.deleteUser(confirmationPassword);
    }
}
