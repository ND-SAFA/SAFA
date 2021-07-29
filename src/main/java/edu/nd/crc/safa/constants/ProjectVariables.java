package edu.nd.crc.safa.constants;

/* Holds constants to magic string variables that may arise
 * during development.
 */
public class ProjectVariables {
    public static final String MAIN_PACKAGE = "edu.nd.crc.safa";

    // SQL database
    public static final String SQL_URL = System.getenv("_MY_SQL_URL");
    public static final String SQL_USERNAME = System.getenv("_MY_SQL_USERNAME");
    public static final String SQL_PASSWORD = System.getenv("_MY_SQL_PASSWORD");
}
