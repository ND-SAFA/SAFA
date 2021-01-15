package edu.nd.crc.safa.importer;
// import sun.awt.windows.WPrinterJob;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Collection;
import java.util.Arrays;

import com.jsoniter.JsonIterator;
import org.springframework.stereotype.Component;

@Component
public class GenerateFlatfile {
    public File createGeneratedFilesDir() throws Exception {
        String dir = "/generatedFilesDir";
        File myDir = new File(dir);

        if (!myDir.exists()) {
            if (!myDir.mkdirs()){
                throw new Exception("Error creating Generated Files folder: Path: /generatedFilesDir");
            }
        }

        if (!myDir.isDirectory()) {
            if (!myDir.delete()){
                throw new Exception("Error deleting Generated Files file: Path: /generatedFilesDir");
            }
            if (!myDir.mkdirs()){
                throw new Exception("Error creating Generated Files folder: Path: /generatedFilesDir");
            }
        }

        return myDir;
    }

    public void generateLinks(String sourcePath, String targetPath, String destPath) throws Exception {
        Path sfile = Paths.get(sourcePath);
        Path tfile = Paths.get(targetPath);
        Path dfile = Paths.get(destPath);

        List<String> sDocs = Files.readAllLines(sfile);
        List<String> tDocs = Files.readAllLines(tfile);
        sDocs.remove(0);
        tDocs.remove(0);
        Map<String, Collection<String>> sTokens = new HashMap<>(), tTokens = new HashMap<>();
        for (String doc : sDocs) {
            String[] parts = doc.split(",");
            String id = parts[1], content = parts[2];
            sTokens.put(id, Arrays.asList(content.split(" ")));
        }
        for (String doc : tDocs) {
            String[] parts = doc.split(",");
            String id = parts[0], content = parts[2];
            tTokens.put(id, Arrays.asList(content.split(" ")));
        }

        VSM vsm = new VSM();
        vsm.buildIndex(tTokens.values());
        List<String> lines = new ArrayList<>();
        lines.add("sid,tid,score");
        for (String sid : sTokens.keySet()) {
            for (String tid : tTokens.keySet()) {
                double score = vsm.getRelevance(sTokens.get(sid), tTokens.get(tid));
                lines.add(String.format("%s,%s,%s", sid, tid, score));
            }
        }
        Files.write(dfile, lines);
    }

    public String generateFiles() throws Exception {
        String fullPath = "/flatfilesDir/generatedData.json";
        
        File file = new File(fullPath);
        if (!file.exists()) {
            return "{ \"success\": true, \"message\": \"Please upload files.\"}";
        }

        String data = new String(Files.readAllBytes(Paths.get(fullPath)));
        if (data.equals("[]")){
            return "{ \"success\": true, \"message\": \"No links needed to be generated.\"}";
        }

        String flatfileDir = "/flatfilesDir";
        String generatedDir = "/generatedFilesDir";
        createGeneratedFilesDir();
        
        JsonIterator iterator = JsonIterator.parse(data);

        List<String> generatedFiles = new ArrayList<String>();
        System.out.println(data);
        System.out.println("Before reading Array");
        while (iterator.readArray()) {
            String filename = "";
            String source = "";
            String target = "";

            for (String field = iterator.readObject(); field != null; field = iterator.readObject()) {
                if (field.equals("filename")) {
                    filename = iterator.readString();
                }
                else if (field.equals("source")) {
                    source = iterator.readString();
                }
                else {
                    target = iterator.readString();
                }
            }

            String destPath = generatedDir + "/" + filename;
            String sourcePath = flatfileDir + "/" + source + ".csv";
            String targetPath = flatfileDir + "/" + target + ".csv";
            System.out.println(destPath);
            System.out.println(sourcePath);
            System.out.println(targetPath);
            // generateLinks(sourcePath, targetPath, destPath);
            generatedFiles.add(filename);
        }
        System.out.println("Done reading Array");
        if (generatedFiles.size() > 0) {
            String requiredFilePath = "/flatfilesDir/requiredData.json";

            File requiredFile = new File(requiredFilePath);
            if (!requiredFile.exists()) {
                return "{ \"success\": false, \"message\": \"Error Path: /flatfilesDir/requiredData.json does not exist.\"}";
            }

            String jsonArr = UploadFlatfile.createJsonArray(generatedFiles);
            String requiredData = new String(Files.readAllBytes(Paths.get(requiredFilePath)));
            String regex =  "\"generatedFiles\":\\[.*\\],\"expectedGeneratedFiles\"";
            String replacement =  String.format("\"generatedFiles\":%s,\"expectedGeneratedFiles\"", jsonArr);
            
            String newRequiredData = requiredData.replaceAll(regex, replacement);
            Files.write(Paths.get(requiredFilePath), newRequiredData.getBytes());
        }
        
        return "{ \"success\": true}";
    } 
}
