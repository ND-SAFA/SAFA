package edu.nd.crc.safa.importer;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Collection;
import java.util.Arrays;
import java.util.Scanner; 
import java.util.Set;
import java.util.HashSet;
import java.io.BufferedReader;
import java.io.FileReader;

import com.jsoniter.JsonIterator;
import org.springframework.stereotype.Component;

@Component
public class GenerateFlatfile {
    public String generateFiles() throws Exception {
        String generatedDir = "/generatedFiles";
        UploadFlatfile.createDirectory(generatedDir);
        
        List<List<String>> data = MySQL.generateInfo();
        System.out.println("Generate Info Works");

        if (data.size() == 0) {
            return "{ \"success\": true, \"message\": \"No links needed to be generated.\"}";
        }
        
        for (List<String> row : data) {
            String sourceTable = row.get(0);
            String targetTable = row.get(1);
            String destTable = row.get(2);
            String destFilePath = String.format("%s/%s.csv", generatedDir, destTable);
            
            generateTraceMatrixFile(sourceTable, targetTable, destFilePath, destTable);
        }

        UploadFlatfile.deleteDirectory(generatedDir);

        return "{ \"success\": true, \"message\": \"Successfully generated links\"}";
    }

    // public String getLinkTypesJSON() throws Exception {
    //     String generatedDir = "/generatedFilesDir";
    //     UploadFlatfile.createDirectory(generatedDir);
    //     Map<String, ArrayList<String>> sourceTargetMap = new HashMap<String, ArrayList<String>>();

    //     String generatedDataPath = generatedDir + "/generatedData.json";
    //     pathErrorChecking(generatedDataPath);

    //     String data = new String(Files.readAllBytes(Paths.get(generatedDataPath)));
    //     if (data.equals("[]")){
    //         throw new Exception("No links available");
    //     }

    //     JsonIterator iterator = JsonIterator.parse(data);
    //     System.out.println("Start reading Array");

    //     while (iterator.readArray()) {
    //         String source = "";
    //         String target = "";

    //         for (String field = iterator.readObject(); field != null; field = iterator.readObject()) {
    //             if (field.equals("filename")) {
    //                 iterator.readString();
    //             }
    //             else if (field.equals("source")) {
    //                 source = iterator.readString();
    //             }
    //             else {
    //                 target = iterator.readString();
    //             }
    //         }

    //         if (source.isEmpty() || target.isEmpty()){
    //             throw new Exception("Error finding source,target links");
    //         }

    //         String key = String.format("\"%s\"", source);
    //         String val = String.format("\"%s\"", target);
            
    //         sourceTargetMap.computeIfAbsent(key, k -> new ArrayList<>()).add(val);
    //     }
    //     System.out.println("Completed reading Array");

    //     String dataDict = sourceTargetMap.toString().replace("=", ":");
    //     System.out.println(dataDict);
    //     return String.format("{ \"success\": true, \"data\": %s}", dataDict);
    // }

    public void generateTraceMatrixFile(String sourceTable, String targetTable, String destFilePath, String destTable) throws Exception {
        List<List<String>> sourceData = MySQL.getArtifactData(sourceTable);
        List<List<String>> targetData = MySQL.getArtifactData(targetTable);

        Map<String, Collection<String>> sTokens = new HashMap<>(), tTokens = new HashMap<>();
        for (List<String> doc : sourceData) {
            sTokens.put(doc.get(0), Arrays.asList(doc.get(2).split(" ")));
        }

        for (List<String> doc : targetData) {
            tTokens.put(doc.get(0), Arrays.asList(doc.get(2).split(" ")));
        }

        VSM vsm = new VSM();
        vsm.buildIndex(tTokens.values());
        List<String> lines = new ArrayList<>();
        lines.add("Source,Target,Score");
        for (String sid : sTokens.keySet()) {
            for (String tid : tTokens.keySet()) {
                double score = vsm.getRelevance(sTokens.get(sid), tTokens.get(tid));
                lines.add(String.format("%s,%s,%s", sid, tid, score));
            }
        }

        Files.write(Paths.get(destFilePath), lines);
        MySQL.createGeneratedTraceMatrixTable(destTable, destFilePath);
    }
}
