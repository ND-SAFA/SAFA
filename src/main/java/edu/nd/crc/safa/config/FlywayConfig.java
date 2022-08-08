package edu.nd.crc.safa.config;

import javax.annotation.PostConstruct;
import javax.sql.DataSource;

import org.flywaydb.core.Flyway;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;

/**
 * Allows app to use Flyway 9 instead of built-in Spring version.
 */
@Configuration
public class FlywayConfig {

    @Autowired
    DataSource dataSource;

    @PostConstruct
    public void runMigrations() {
        Flyway flyway = Flyway.configure().dataSource(dataSource).load();
        flyway.repair();
        flyway.baseline();
        flyway.migrate();
    }
}
