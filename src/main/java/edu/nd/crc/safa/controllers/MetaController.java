package edu.nd.crc.safa.controllers;

import edu.nd.crc.safa.database.Neo4J;
import edu.nd.crc.safa.importer.MySQL;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MetaController {
    @GetMapping("/")
    public ServerResponse root() {
        return new ServerResponse("Hello World");
    }

    @GetMapping("/connections")
    public ServerResponse test_service_connections() throws Exception {
        (new Neo4J()).verifyConnectivity();

        MySQL sql = new MySQL();
        sql.verifyConnection();
        return new ServerResponse("Connected Neo4J and MySQL!");
    }
}
