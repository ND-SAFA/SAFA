package edu.nd.crc.safa.controllers;

import edu.nd.crc.safa.importer.MySQL;
import edu.nd.crc.safa.output.responses.ServerResponse;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MetaController {

    MySQL sql;

    @Autowired
    public MetaController(MySQL sql) {
        this.sql = sql;
    }

    @GetMapping("/")
    public ServerResponse root() {
        return new ServerResponse("Hello World");
    }

    @GetMapping("/connections")
    public ServerResponse test_service_connections() throws UnsupportedOperationException {
        throw new UnsupportedOperationException("connections route is under construction");
    }
}
