package edu.nd.crc.safa.controllers;

import edu.nd.crc.safa.responses.ProjectCreationResponse;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class ProjectController {

    @PostMapping(value = "/projects/flat-files")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public ServerResponse uploadProjectFiles(@RequestParam("files") MultipartFile[] files) {
        String[] filesReceived = new String[files.length];

        for (int i = 0; i < files.length; i++) {
            filesReceived[i] = files[i].getOriginalFilename();
        }

        return new ServerResponse(new ProjectCreationResponse(filesReceived));
    }
}

