package edu.nd.crc.safa.server.controllers;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.app.UserAppEntity;
import edu.nd.crc.safa.server.entities.db.SafaUser;
import edu.nd.crc.safa.server.repositories.projects.SafaUserRepository;

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

    private final SafaUserRepository safaUserRepository;
    private final PasswordEncoder passwordEncoder;

    @Autowired
    public SafaUserController(ResourceBuilder resourceBuilder,
                              SafaUserRepository safaUserRepository,
                              PasswordEncoder passwordEncoder) {
        super(resourceBuilder);
        this.safaUserRepository = safaUserRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @PostMapping(AppRoutes.Accounts.CREATE_ACCOUNT)
    public UserAppEntity createNewUser(@RequestBody SafaUser newUser) {
        newUser.setPassword(this.passwordEncoder.encode(newUser.getPassword()));
        this.safaUserRepository.save(newUser);
        return new UserAppEntity(newUser);
    }
}
