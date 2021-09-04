package edu.nd.crc.safa.server.controllers;

import edu.nd.crc.safa.server.responses.ServerResponse;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MetaController {
    @GetMapping("/")
    public ServerResponse root() {
        return new ServerResponse("Hello World");
    }
}
