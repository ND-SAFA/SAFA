package edu.nd.crc.safa.config;

import javax.sql.DataSource;

import org.flywaydb.core.Flyway;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Allows app to use Flyway 9 instead of built-in Spring version.
 */
@Configuration
public class FlywayConfig {

    @Bean(name = "Flyway")
    @Autowired
    public Flyway runMigrations(DataSource dataSource) {
        Flyway flyway = Flyway.configure().dataSource(dataSource).load();
        flyway.repair();
        flyway.baseline();
        flyway.migrate();
        return flyway;
    }
}
