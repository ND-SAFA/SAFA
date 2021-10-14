package edu.nd.crc.safa.config;

import java.util.Properties;

import edu.nd.crc.safa.server.messages.ServerError;

public class DatabaseProperties {

    private final SQLServers sqlType;
    public String url;
    public String username;
    public String password;

    public DatabaseProperties(String url, String username, String password) {
        this.url = url;
        this.username = username;
        this.password = password;

        String MYSQL_ID = "mysql";
        String h2_ID = "h2";

        String prodSqlUrl = System.getenv("_MY_SQL_URL");
        String prodSqlUsername = System.getenv("_MY_SQL_USERNAME");
        String prodSqlPassword = System.getenv("_MY_SQL_PASSWORD");

        if (prodSqlUrl != null
            && prodSqlUsername != null
            && prodSqlPassword != null) {
            this.url = prodSqlUrl;
            this.username = prodSqlUsername;
            this.password = prodSqlPassword;
        }

        if (this.url.toLowerCase().contains(MYSQL_ID)) {
            this.sqlType = SQLServers.MYSQL;
        } else if (this.url.toLowerCase().contains(h2_ID)) {
            this.sqlType = SQLServers.H2;
        } else {
            throw new RuntimeException("Hibernate dialect not supported for connection string:" + this.url);
        }
    }

    public String getDriverClassName() {
        switch (sqlType) {
            case MYSQL:
                return "com.mysql.cj.jdbc.Driver";
            case H2:
                return "org.h2.Driver";
            default:
                throw new RuntimeException("Could not identify driver for server type:" + sqlType);
        }
    }

    public Properties getConnectionProperties() throws ServerError {
        assertValidCredentials();
        Properties hibernateProperties = new Properties();
        hibernateProperties.setProperty("hibernate.dialect", getHibernateDialect());
        hibernateProperties.setProperty("hibernate.hbm2ddl.auto", "create");
        return hibernateProperties;
    }

    private String getHibernateDialect() {
        switch (sqlType) {
            case MYSQL:
                return "org.hibernate.dialect.MySQL5Dialect";
            case H2:
                return "org.hibernate.dialect.H2Dialect";
            default:
                throw new RuntimeException("Hibernate dialect not supported for connection string:" + url);
        }
    }

    public void assertValidCredentials() throws ServerError {
        if (url == null) {
            throw new ServerError("MySQL URL is null");
        }
        if (username == null) {
            throw new ServerError("MySQL username is null");
        }
        if (password == null) {
            throw new ServerError("MySQL password is null");
        }
    }
}
