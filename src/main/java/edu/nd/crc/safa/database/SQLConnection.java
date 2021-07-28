package edu.nd.crc.safa.database;

import static edu.nd.crc.safa.constants.ProjectVariables.SQL_PASSWORD;
import static edu.nd.crc.safa.constants.ProjectVariables.SQL_URL;
import static edu.nd.crc.safa.constants.ProjectVariables.SQL_USERNAME;

import java.util.List;
import java.util.Properties;

import javax.sql.DataSource;

import edu.nd.crc.safa.constants.ProjectVariables;
import edu.nd.crc.safa.error.ServerError;

import com.github.fluent.hibernate.cfg.scanner.EntityScanner;
import org.apache.commons.dbcp2.BasicDataSource;
import org.hibernate.boot.MetadataSources;

/**
 * Responsible for holding and providing configuration setting
 * to the SQL database.
 */
public class SQLConnection {
    final String DIALECT_PROP = "hibernate.dialect";
    final String MYSQL_DIALECT = "org.hibernate.dialect.MySQL5Dialect";
    final String h2_DIALECT = "org.hibernate.dialect.H2Dialect";
    final String MYSQL_ID = "mysql";
    final String H2_ID = "h2";
    final String TABLE_CREATION_PROP = "hibernate.hbm2ddl.auto";

    public DataSource dataSource() throws ServerError {
        assertValidCredentials();
        BasicDataSource dataSource = new BasicDataSource();

        dataSource.setUrl(SQL_URL);
        dataSource.setUsername(ProjectVariables.SQL_USERNAME);
        dataSource.setPassword(ProjectVariables.SQL_PASSWORD);

        return dataSource;
    }

    public Properties getConnectionProperties() throws ServerError {
        assertValidCredentials();

        String queryURL = SQL_URL.toLowerCase();
        Properties hibernateProperties = new Properties();

        if (queryURL.contains(MYSQL_ID)) {
            hibernateProperties.setProperty(DIALECT_PROP, MYSQL_DIALECT);
        } else if (queryURL.contains(H2_ID)) {
            hibernateProperties.setProperty(DIALECT_PROP, h2_DIALECT);
        } else {
            throw new RuntimeException("Hibernate dialect not supported for connection string:" + SQL_URL);
        }
        hibernateProperties.setProperty(TABLE_CREATION_PROP, "create");

        return hibernateProperties;
    }

    public MetadataSources getEntitiesMetaData() {
        List<Class<?>> classes = EntityScanner.scanPackages(ProjectVariables.MAIN_PACKAGE).result();

        MetadataSources metadataSources = new MetadataSources();
        for (Class<?> annotatedClass : classes) {
            metadataSources.addAnnotatedClass(annotatedClass);
        }
        return metadataSources;
    }

    private void assertValidCredentials() throws ServerError {
        if (SQL_URL == null) {
            throw new ServerError("MySQL URL is null");
        }
        if (SQL_USERNAME == null) {
            throw new ServerError("MySQL username is null");
        }
        if (SQL_PASSWORD == null) {
            throw new ServerError("MySQL password is null");
        }
    }
}
