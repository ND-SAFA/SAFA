package edu.nd.crc.safa;
import org.neo4j.ogm.session.SessionFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.data.neo4j.repository.config.EnableNeo4jRepositories;
import org.springframework.data.neo4j.transaction.Neo4jTransactionManager;
import org.springframework.transaction.annotation.EnableTransactionManagement;

@SpringBootApplication
@EnableNeo4jRepositories("edu.nd.crc.safa.repositories")
@EnableTransactionManagement
public class MainApplication {

  @Value("${neo4j.uri}") String neo4jURI;
  @Value("${neo4j.username}") String neo4jUser;
  @Value("${neo4j.password}") String neo4jPassword;

  @Bean
  public SessionFactory sessionFactory() {
      // with domain entity base package(s)
      return new SessionFactory(configuration(), "edu.nd.crc.safa.domain");
  }

  @Bean
  public org.neo4j.ogm.config.Configuration configuration() {
    return new org.neo4j.ogm.config.Configuration.Builder()
      .uri(neo4jURI)
      .credentials(neo4jUser, neo4jPassword)
      .build();
  }

  @Bean
  public Neo4jTransactionManager transactionManager() {
      return new Neo4jTransactionManager(sessionFactory());
  }

  public static void main(String[] args) {
      SpringApplication.run(MainApplication.class, args);
  }
}