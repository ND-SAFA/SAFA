package edu.nd.crc.safa;

import javax.persistence.EntityManagerFactory;
import javax.sql.DataSource;

import edu.nd.crc.safa.config.DatabaseProperties;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.server.responses.ServerError;

import org.apache.commons.dbcp2.BasicDataSource;
import org.hibernate.jpa.HibernatePersistenceProvider;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean;
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

    DatabaseProperties dbProperties;

    @Bean
    public DataSource getDataSource(@Value(value = "${sql.url}") String url,
                                    @Value(value = "${sql.username}") String username,
                                    @Value(value = "${sql.password}") String password) throws ServerError {
        this.dbProperties = new DatabaseProperties(url, username, password);
        dbProperties.assertValidCredentials();
        BasicDataSource dataSource = new BasicDataSource();

        dataSource.setUrl(dbProperties.url);
        dataSource.setUsername(dbProperties.username);
        dataSource.setPassword(dbProperties.password);
        dataSource.setDriverClassName(dbProperties.getDriverClassName());

        return dataSource;
    }

    @Bean
    public EntityManagerFactory entityManagerFactory(DataSource dataSource) throws ServerError {
        LocalContainerEntityManagerFactoryBean emf = new LocalContainerEntityManagerFactoryBean();
        HibernatePersistenceProvider provider = new HibernatePersistenceProvider();
        emf.setDataSource(dataSource);
        emf.setJpaProperties(dbProperties.getConnectionProperties());
        emf.setPersistenceProvider(provider);
        emf.setPackagesToScan(ProjectVariables.ENTITIES_PACKAGE);
        emf.afterPropertiesSet();
        return emf.getNativeEntityManagerFactory();
    }
}
