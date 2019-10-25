package edu.nd.crc.safa;
import org.neo4j.driver.v1.AuthToken;
import org.neo4j.driver.v1.AuthTokens;
import org.neo4j.driver.v1.Driver;
import org.neo4j.driver.v1.GraphDatabase;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class MainApplication {

  @Value("${neo4j.host}") String neo4jHost;
  @Value("${neo4j.port}") String neo4jPort;
  @Value("${neo4j.username}") String neo4jUser;
  @Value("${neo4j.password}") String neo4jPassword;
  @Value("${neo4j.scheme:bolt}") String neo4jScheme;
  @Value("${neo4j.routingPolicy:}") String neo4jRoutingPolicy;
  @Value("${neo4j.authType:basic}") String neo4jAuthType;
  @Value("${neo4j.ticket:}") String neo4jKerberosTicket;
  
  public static void main(String[] args) {
    SpringApplication.run(MainApplication.class, args);
  }

  @Bean
  public Driver neo4jDriver() {
    String URI = getNeo4jUri();
    AuthToken token = getNeo4jAuthToken();
    return GraphDatabase.driver(URI, token);
  }

  public String getNeo4jUri() {
    String uri = String.format("%s://%s:%s", neo4jScheme, neo4jHost, neo4jPort);
    if ( neo4jScheme == "bolt+routing" && neo4jRoutingPolicy != null ) {
      uri += "?policy="+ neo4jRoutingPolicy;
    }
    return uri;
  }

  public AuthToken getNeo4jAuthToken() {
    switch ( neo4jAuthType ) {
      case "basic":
        return AuthTokens.basic(neo4jUser, neo4jPassword);
      case "kerberos":
        return AuthTokens.kerberos(neo4jKerberosTicket);
      default:
        return AuthTokens.none();
    }
  }
  
  // @Bean
  // public SessionFactory sessionFactory() {
  //     // with domain entity base package(s)
  //     SessionFactory sessionFactory = new SessionFactory(configuration(), "edu.nd.crc.safa.domain");
  //     sessionFactory.setLoadStrategy(LoadStrategy.SCHEMA_LOAD_STRATEGY);
  //     return sessionFactory;
  // }

  // @Bean
  // public org.neo4j.ogm.config.Configuration configuration() {
  //   return new org.neo4j.ogm.config.Configuration.Builder()
  //     .uri(neo4jURI)
  //     .credentials(neo4jUser, neo4jPassword)
  //     .build();
  // }

  // @Bean
  // public Neo4jTransactionManager transactionManager() {
  //     return new Neo4jTransactionManager(sessionFactory());
  // }
}