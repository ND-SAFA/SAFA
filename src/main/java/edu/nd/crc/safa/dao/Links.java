package edu.nd.crc.safa.dao;

import java.util.List;

public class Links {
    public static class Link {
        public String target;
        public String source;
        public int approval;
    }

    public List<Link> links;
}
