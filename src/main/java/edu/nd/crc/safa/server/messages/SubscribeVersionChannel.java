package edu.nd.crc.safa.server.messages;

public class SubscribeVersionChannel {

    int majorVersion;
    int minorVersion;

    public SubscribeVersionChannel() {
    }

    public int getMajorVersion() {
        return majorVersion;
    }

    public void setMajorVersion(int majorVersion) {
        this.majorVersion = majorVersion;
    }

    public int getMinorVersion() {
        return minorVersion;
    }

    public void setMinorVersion(int minorVersion) {
        this.minorVersion = minorVersion;
    }
}
