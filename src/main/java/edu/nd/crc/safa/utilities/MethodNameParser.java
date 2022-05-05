package edu.nd.crc.safa.utilities;

public class MethodNameParser {

    public static int getNumberAfterPrefix(String originalMethodName, String prefix) {
        String nameStartingWithNumber = originalMethodName.substring(prefix.length());
        StringBuilder stepStr = new StringBuilder();
        for (int i = 0; i < nameStartingWithNumber.length(); i++) {
            char nextPossibleDigit = nameStartingWithNumber.charAt(i);
            if (Character.isDigit(nextPossibleDigit)) {
                stepStr.append(nextPossibleDigit);
            } else {
                break;
            }
        }
        if (stepStr.length() == 0) {
            throw new RuntimeException("Could not parse step:" + originalMethodName);
        }
        return Integer.parseInt(stepStr.toString());
    }
}
