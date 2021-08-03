package edu.nd.crc.safa.database.connection;

import static edu.nd.crc.safa.constants.DatabaseVariables.SQL_URL;
import static edu.nd.crc.safa.constants.DatabaseVariables.SQL_USERNAME;

import java.util.List;
import java.util.Properties;

import edu.nd.crc.safa.constants.DatabaseVariables;
import edu.nd.crc.safa.constants.ProjectVariables;
import edu.nd.crc.safa.server.error.ServerError;

import com.github.fluent.hibernate.cfg.scanner.EntityScanner;
import org.hibernate.boot.MetadataSources;

/**
 * Responsible for holding and providing configuration setting
 * for the SQL connection.
 */
public class SQLConnection {

    public static Properties getConnectionProperties() throws ServerError {
        assertValidCredentials();
        Properties hibernateProperties = new Properties();
        hibernateProperties.setProperty("hibernate.dialect", getHibernateDialect());
        hibernateProperties.setProperty("hibernate.hbm2ddl.auto", "create");
        return hibernateProperties;
    }

    public static MetadataSources getEntitiesMetaData() {
        List<Class<?>> classes = EntityScanner.scanPackages(ProjectVariables.MAIN_PACKAGE).result();

        MetadataSources metadataSources = new MetadataSources();
        for (Class<?> annotatedClass : classes) {
            metadataSources.addAnnotatedClass(annotatedClass);
        }
        return metadataSources;
    }

    public static void assertValidCredentials() throws ServerError {
        if (SQL_URL == null) {
            throw new ServerError("MySQL URL is null");
        }
        if (SQL_USERNAME == null) {
            throw new ServerError("MySQL username is null");
        }
        if (DatabaseVariables.SQL_PASSWORD == null) {
            throw new ServerError("MySQL password is null");
        }
    }

    public static String getDriverClassName() {
        switch (DatabaseVariables.SQL_TYPE) {
            case MYSQL:
                return "com.mysql.cj.jdbc.Driver";
            case H2:
                return "org.h2.Driver";
            default:
                throw new RuntimeException("Could not identify driver for server type:" + DatabaseVariables.SQL_TYPE);
        }
    }

    private static String getHibernateDialect() {
        switch (DatabaseVariables.SQL_TYPE) {
            case MYSQL:
                return "org.hibernate.dialect.MySQL5Dialect";
            case H2:
                return "org.hibernate.dialect.H2Dialect";
            default:
                throw new RuntimeException("Hibernate dialect not supported for connection string:" + SQL_URL);
        }
    }
}
