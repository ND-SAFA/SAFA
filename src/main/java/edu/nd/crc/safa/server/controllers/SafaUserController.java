package edu.nd.crc.safa.server.controllers;

import edu.nd.crc.safa.config.Routes;
import edu.nd.crc.safa.server.entities.db.SafaUser;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.services.SafaUserService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@CrossOrigin
@RestController
public class SafaUserController extends BaseController {

    final String createAccountLink = "create-account";

    SafaUserService safaUserService;

    @Autowired
    public SafaUserController(ProjectRepository projectRepository,
                              ProjectVersionRepository projectVersionRepository,
                              SafaUserService safaUserService) {
        super(projectRepository, projectVersionRepository);
        this.safaUserService = safaUserService;
    }

    @PostMapping(Routes.createAccountLink)
    public SafaUser createNewUser(@RequestBody SafaUser newUser) {
        return this.safaUserService.createNewUser(newUser);
    }
}
