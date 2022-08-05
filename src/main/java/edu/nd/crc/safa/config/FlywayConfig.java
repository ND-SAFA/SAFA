package edu.nd.crc.safa.config;

import javax.sql.DataSource;

import org.flywaydb.core.Flyway;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Responsible for fixing an broken migrations and attempting to re-apply them.
 */
@Configuration
public class FlywayConfig {

    @Autowired
    DataSource dataSource;

    @Bean
    public Flyway runMigrations() {
        Flyway flyway = Flyway.configure().dataSource(dataSource).load();
        flyway.repair();
        flyway.migrate();
        return flyway;
    }
}
