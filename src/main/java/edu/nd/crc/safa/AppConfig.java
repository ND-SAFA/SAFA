package edu.nd.crc.safa;

import java.io.IOException;

import edu.nd.crc.safa.constants.ProjectVariables;
import edu.nd.crc.safa.database.SQLConnection;
import edu.nd.crc.safa.error.ServerError;

import org.hibernate.SessionFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.orm.hibernate5.LocalSessionFactoryBean;

/**
 * Responsible for setting up AppContext through annotations
 * and holding all the beans.
 */
@Configuration
@ComponentScan(ProjectVariables.MAIN_PACKAGE)
public class AppConfig {

    @Bean
    public SessionFactory createSessionFactory() throws ServerError, IOException {
        LocalSessionFactoryBean sessionFactory = new LocalSessionFactoryBean();

        SQLConnection sqlConnection = new SQLConnection();
        sessionFactory.setMetadataSources(sqlConnection.getEntitiesMetaData());
        sessionFactory.setDataSource(sqlConnection.dataSource());
        sessionFactory.setHibernateProperties(sqlConnection.getConnectionProperties());
        sessionFactory.afterPropertiesSet();

        return sessionFactory.getObject();
    }
}
