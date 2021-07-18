package edu.nd.crc.safa;

import org.neo4j.driver.AuthToken;
import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.Config;
import org.neo4j.driver.Driver;
import org.neo4j.driver.GraphDatabase;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class MainApplication {

    // Neo4J Credentials
    String neo4jURI = System.getenv("_NEO4J_URI");
    String neo4jUser = System.getenv("_NEO4J_USERNAME");
    String neo4jPassword = System.getenv("_NEO4J_PASSWORD");

    public static void main(String[] args) {
        SpringApplication.run(MainApplication.class, args);
    }

    @Bean
    public Driver neo4jDriver() {
        if (neo4jURI == null || neo4jUser == null || neo4jPassword == null) {
            throw new RuntimeException("Neo4J instance credentials are null");
        }
        AuthToken token = AuthTokens.basic(neo4jUser, neo4jPassword);
        return GraphDatabase.driver(neo4jURI, AuthTokens.basic(neo4jUser, neo4jPassword), Config.defaultConfig());
    }
}
