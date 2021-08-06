package edu.nd.crc.safa.configuration;

public class DatabaseVariables {
    public static final String SQL_URL = System.getenv("_MY_SQL_URL");
    public static final String SQL_USERNAME = System.getenv("_MY_SQL_USERNAME");
    public static final String SQL_PASSWORD = System.getenv("_MY_SQL_PASSWORD");

    public static SQLServers SQL_TYPE;

    private static final String MYSQL_ID = "mysql";
    private static final String H2_ID = "h2";

    static {
        if (SQL_URL.toLowerCase().contains(MYSQL_ID)) {
            SQL_TYPE = SQLServers.MYSQL;
        } else if (SQL_URL.toLowerCase().contains(H2_ID)) {
            SQL_TYPE = SQLServers.H2;
        } else {
            throw new RuntimeException("Hibernate dialect not supported for connection string:" + SQL_URL);
        }
    }
}
