package edu.nd.crc.safa.database;

import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.Config;
import org.neo4j.driver.Driver;
import org.neo4j.driver.GraphDatabase;
import org.neo4j.driver.Session;
import org.springframework.stereotype.Component;

@Component
public class Neo4J {

    protected String neo4jURI = System.getenv("_NEO4J_URI");
    protected String neo4jUser = System.getenv("_NEO4J_USERNAME");
    protected String neo4jPassword = System.getenv("_NEO4J_PASSWORD");

    private Driver driver;

    protected Driver getDriver() {
        System.out.println("getting neo4j driver");

        if (driver != null) {
            return driver;
        } else if (neo4jURI == null) {
            throw new RuntimeException("Neo4J Uri is null");
        } else if (neo4jUser == null) {
            throw new RuntimeException("Neo4J neo4jUser is null");
        } else if (neo4jPassword == null) {
            throw new RuntimeException("Neo4J Password is null");
        }
        //TODO: Enable earlier auth tokens
        driver = GraphDatabase.driver(neo4jURI,
            AuthTokens.basic(neo4jUser, neo4jPassword),
            Config.defaultConfig());
        return driver;
    }

    public Session createSession() {
        System.out.println("Creating session");
        return getDriver().session();
    }

    public void verifyConnectivity() {
        getDriver().verifyConnectivity();
    }

    public void close() {
        getDriver().close();
    }
}
