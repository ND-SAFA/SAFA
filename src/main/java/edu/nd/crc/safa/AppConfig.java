package edu.nd.crc.safa;

import static edu.nd.crc.safa.constants.DatabaseVariables.SQL_URL;

import java.io.IOException;

import javax.sql.DataSource;

import edu.nd.crc.safa.constants.DatabaseVariables;
import edu.nd.crc.safa.constants.ProjectVariables;
import edu.nd.crc.safa.database.connection.SQLConnection;
import edu.nd.crc.safa.server.error.ServerError;

import org.apache.commons.dbcp2.BasicDataSource;
import org.hibernate.SessionFactory;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.orm.hibernate5.LocalSessionFactoryBean;
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
    public SessionFactory createSessionFactory() throws ServerError, IOException {
        LocalSessionFactoryBean sessionFactory = new LocalSessionFactoryBean();

        sessionFactory.setMetadataSources(SQLConnection.getEntitiesMetaData());
        sessionFactory.setHibernateProperties(SQLConnection.getConnectionProperties());
        sessionFactory.setDataSource(getDataSource());
        sessionFactory.afterPropertiesSet();

        return sessionFactory.getObject();
    }

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
}
