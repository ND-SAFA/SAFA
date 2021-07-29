package edu.nd.crc.safa.controllers;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ProjectController {

    @PostMapping("/projects/flat-files")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void uploadProjectFiles() {

    }
}
