package edu.nd.crc.safa;

import java.util.Map;
import javax.persistence.EntityManagerFactory;
import javax.sql.DataSource;

import edu.nd.crc.safa.config.DatabaseProperties;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.config.SQLServers;
import edu.nd.crc.safa.server.messages.ServerError;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
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

        Map<String, String> env = System.getenv();
        HikariConfig config = new HikariConfig();
        if (env.containsKey("INSTANCE_CONNECTION_NAME")
            && !env.get("INSTANCE_CONNECTION_NAME").equals("")
            && this.dbProperties.getSqlType() != SQLServers.H2) {

            String instanceConnectionName = env.get("INSTANCE_CONNECTION_NAME");
            System.out.println("INSTANCE CONNECTION NAME:" + instanceConnectionName);
            String databaseName = env.get("DB_NAME");

            config.setJdbcUrl(String.format("jdbc:mysql:///%s", databaseName));
            config.setUsername(username);
            config.setPassword(password);

            config.addDataSourceProperty("socketFactory", "com.google.cloud.sql.mysql.SocketFactory");
            config.addDataSourceProperty("cloudSqlInstance", instanceConnectionName);
            config.addDataSourceProperty("ipTypes", "PUBLIC,PRIVATE");
        } else {
            System.out.println("BASIC CONNECTION:" + dbProperties.url);
            config.setJdbcUrl(dbProperties.url);
            config.setUsername(dbProperties.username);
            config.setPassword(dbProperties.password);
            config.setDriverClassName(dbProperties.getDriverClassName());
        }
        return new HikariDataSource(config);
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
