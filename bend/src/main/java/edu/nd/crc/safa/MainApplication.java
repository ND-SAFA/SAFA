package edu.nd.crc.safa;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.flyway.FlywayAutoConfiguration;
import org.springframework.boot.context.properties.ConfigurationPropertiesScan;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.web.socket.config.annotation.EnableWebSocket;
import org.springframework.web.socket.config.annotation.EnableWebSocketMessageBroker;

/**
 * The entry point into the application.
 */
@SpringBootApplication(exclude = FlywayAutoConfiguration.class)
@EnableWebSocket
@EnableWebSocketMessageBroker
@ConfigurationPropertiesScan
public class MainApplication {
    private static AnnotationConfigApplicationContext applicationContext;

    public static void main(String[] args) {
        SpringApplication.run(MainApplication.class, args);
    }
}
