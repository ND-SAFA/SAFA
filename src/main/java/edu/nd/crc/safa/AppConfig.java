package edu.nd.crc.safa;

import static edu.nd.crc.safa.constants.DatabaseVariables.SQL_URL;

import javax.persistence.EntityManagerFactory;
import javax.sql.DataSource;

import edu.nd.crc.safa.constants.DatabaseVariables;
import edu.nd.crc.safa.constants.ProjectVariables;
import edu.nd.crc.safa.database.configuration.SQLConnection;
import edu.nd.crc.safa.output.error.ServerError;

import org.apache.commons.dbcp2.BasicDataSource;
import org.hibernate.jpa.HibernatePersistenceProvider;
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

    @Bean
    public DataSource getDataSource() throws ServerError {
        SQLConnection.assertValidCredentials();
        BasicDataSource dataSource = new BasicDataSource();

        dataSource.setUrl(SQL_URL);
        dataSource.setUsername(DatabaseVariables.SQL_USERNAME);
        dataSource.setPassword(DatabaseVariables.SQL_PASSWORD);
        dataSource.setDriverClassName(SQLConnection.getDriverClassName());

        return dataSource;
    }

    @Bean
    public EntityManagerFactory entityManagerFactory() throws ServerError {
        LocalContainerEntityManagerFactoryBean emf = new LocalContainerEntityManagerFactoryBean();
        HibernatePersistenceProvider provider = new HibernatePersistenceProvider();
        emf.setDataSource(this.getDataSource());
        emf.setJpaProperties(SQLConnection.getConnectionProperties());
        emf.setPersistenceProvider(provider);
        emf.setPackagesToScan(ProjectVariables.ENTITIES_PACKAGE);
        emf.afterPropertiesSet();
        return emf.getNativeEntityManagerFactory();
    }
}
