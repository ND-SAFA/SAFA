package edu.nd.crc.safa.importer.flatfile;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.error.ServerError;
import edu.nd.crc.safa.importer.MySQL;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class TIMCreator {

    private MySQL sql;

    @Autowired
    public TIMCreator(MySQL sql) {
        this.sql = sql;
    }

    public static class TimBackend {
        public List<List<String>> artifacts = new ArrayList<List<String>>();
        public List<List<String>> traces = new ArrayList<List<String>>();
    }

    public TimBackend getTimFile() throws ServerError {
        TimBackend timBackend = new TimBackend();

        List<List<String>> artifact_rows = sql.getTimArtifactData();
        for (List<String> artifact_row : artifact_rows) {
            List<String> artifacts = new ArrayList<String>();

            String artifact = String.format("\"%s\"", artifact_row.get(0));
            String filename = String.format("\"%s\"", artifact_row.get(2));

            artifacts.add(artifact);
            artifacts.add(filename);
            timBackend.artifacts.add(artifacts);
        }

        List<List<String>> trace_rows = sql.getTimTraceData();
        for (List<String> trace_row : trace_rows) {
            List<String> traces = new ArrayList<String>();

            String trace = String.format("\"%s\"", trace_row.get(0));
            String source = String.format("\"%s\"", trace_row.get(1));
            String target = String.format("\"%s\"", trace_row.get(2));
            String filename = String.format("\"%s\"", trace_row.get(5));

            if (trace_rows.get(3).equals('1')) {
                filename = String.format("\"generateLinks\"");
            }

            traces.add(trace);
            traces.add(source);
            traces.add(target);
            traces.add(filename);

            timBackend.traces.add(traces);
        }

        return timBackend;
    }
}
