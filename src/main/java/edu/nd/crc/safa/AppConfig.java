package edu.nd.crc.safa;

import edu.nd.crc.safa.config.ProjectVariables;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.boot.autoconfigure.orm.jpa.JpaProperties;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.transaction.annotation.EnableTransactionManagement;

/**
 * Responsible for setting up AppContext through annotations
 * and holding all the beans.
 */
@Configuration
@EnableAutoConfiguration
@EntityScan(ProjectVariables.MAIN_PACKAGE)
@ComponentScan(ProjectVariables.MAIN_PACKAGE)
@EnableJpaRepositories(ProjectVariables.MAIN_PACKAGE)
@EnableTransactionManagement
public class AppConfig {

    @Autowired
    public AppConfig(JpaProperties properties) {
        System.out.println("Properties:" + properties.getProperties());
        System.out.println("Is ddl-on:" + properties.isGenerateDdl());
    }
}
