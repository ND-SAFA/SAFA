package edu.nd.crc.safa.config;

import java.util.HashMap;
import java.util.Map;
import javax.sql.DataSource;

import org.flywaydb.core.Flyway;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.flyway.FlywayMigrationInitializer;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Allows app to use Flyway 9 instead of built-in Spring version.
 */
@Configuration
public class FlywayConfig {

    @Value("${spring.flyway.baselineOnMigrate}")
    private boolean baselineOnMigrate;

    @Bean(name = "Flyway")
    @Autowired
    public Flyway runMigrations(DataSource dataSource) {
        Flyway flyway = Flyway
            .configure()
            .dataSource(dataSource)
            .baselineOnMigrate(baselineOnMigrate)
            .outOfOrder(false)
            .placeholders(flywayPlaceholders())
            .load();

        flyway.repair();
        flyway.baseline();
        flyway.migrate();

        return flyway;
    }

    @Bean(name = "flywayPlaceholders")
    @ConfigurationProperties(prefix = "spring.flyway.placeholders")
    public Map<String, String> flywayPlaceholders() {
        return new HashMap<>();
    }

    @Bean
    public FlywayMigrationInitializer flywayMigrationInitializer(Flyway flyway) {
        return new FlywayMigrationInitializer(flyway);
    }
}
