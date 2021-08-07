package edu.nd.crc.safa.config;

import edu.nd.crc.safa.responses.ServerError;

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

    protected Driver getDriver() throws ServerError {
        if (driver != null) {
            return driver;
        } else if (neo4jURI == null) {
            throw new ServerError("Neo4J URI is null");
        } else if (neo4jUser == null) {
            throw new ServerError("Neo4J username is null");
        } else if (neo4jPassword == null) {
            throw new ServerError("Neo4J password is null");
        }
        //TODO: Enable earlier auth tokens
        driver = GraphDatabase.driver(neo4jURI,
            AuthTokens.basic(neo4jUser, neo4jPassword),
            Config.defaultConfig());
        return driver;
    }

    public Session createSession() throws ServerError {
        return getDriver().session();
    }

    public void close() throws ServerError {
        Driver driver = getDriver();
        if (driver != null) {
            driver.close();
        }
    }
}
