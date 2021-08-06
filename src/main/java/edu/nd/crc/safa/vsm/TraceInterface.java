package edu.nd.crc.safa.vsm;

import java.util.Collection;

public interface TraceInterface {
    double getRelevance(Collection<String> source, Collection<String> target);
}
