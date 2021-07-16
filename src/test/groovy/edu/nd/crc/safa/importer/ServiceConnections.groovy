package edu.nd.crc.safa.importer

import org.neo4j.driver.AuthTokens
import org.neo4j.driver.Config
import org.neo4j.driver.GraphDatabase
import spock.lang.Specification

class ServiceConnections extends Specification {
    def "MySQL Connection"() {
        System.out.println("HELLO")

        def sql = new MySQL();

        expect:
        def tables = sql.getTableNames()
        tables.size() > 0
    }

    def "Neo4J Connection"() {

        def uri = System.getenv("_NEO4J_URI");
        def username = System.getenv("_NEO4J_USERNAME");
        def password = System.getenv("_NEO4J_PASSWORD");
        System.out.println("Neo4J" + uri + ":" + username);
        def driver = GraphDatabase.driver(
                uri,
                AuthTokens.basic(username, password),
                Config.defaultConfig());
        expect:
        driver.verifyConnectivity()
    }
}
