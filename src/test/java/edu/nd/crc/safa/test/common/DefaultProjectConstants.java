package edu.nd.crc.safa.test.common;

/**
 * The testing constants for the "before" test project.
 */
public class DefaultProjectConstants {
    public static class Entities {
        public static final int N_TYPES = 4;
        public static final int N_DESIGNS = 14;
        public static final int N_REQUIREMENTS = 5;
        public static final int N_HAZARDS = 5;
        public static final int N_ENV_ASSUMPTIONS = 1;
        public static final int N_ARTIFACTS = N_DESIGNS + N_REQUIREMENTS + N_HAZARDS + N_ENV_ASSUMPTIONS;
        public static final int N_LINKS = 22; //23 but there exist an invalid one
    }

    public static class File {
        public static final String DESIGN_FILE = "Design.csv";
    }
}
