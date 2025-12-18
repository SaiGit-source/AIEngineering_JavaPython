package config;


import jakarta.annotation.PostConstruct;
import org.springframework.ai.document.Document;
import org.springframework.ai.reader.TextReader;
import org.springframework.ai.transformer.splitter.TokenTextSplitter;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Component;

import java.util.List;

// Store the data (product_details.txt) into vector store or initialize data
@Component
public class DataInit {


    // unfortunately we dont have the bean for VectorStore that Spring will inject, so we cant use @Autowired, we have to create a class for AppConfig()
    @Autowired
    private VectorStore vectorStore;

    // we got to call this method initData() when we load the application
    // Either manually call the method or use PostConstruct()
    @PostConstruct
    public void initData(){
        TextReader textReader = new TextReader(new ClassPathResource("product_details.txt"));
        // save data into vector store
        // click on the add() method to see what it accepts "void add(List<Document> documents);" it is in the VectorStore class
        // when you work with huge amount of data, we cant just put everything in one place, what you do it, you break down this data into chunks. You store those chunks in database and we call them as "Documents"
        // one chunk becomes one row for you
        // we can break down into chunk using TokenTextSplitter
        //TokenTextSplitter splitter = new TokenTextSplitter(); // customize the document retrieval. if you have a very big text but if you create documents with small chunkSizes then you will have way more documents, which we dont want. we got to find the trade-offs between TextSize and Num of documents (based on chunk-size)
        TokenTextSplitter splitter = new TokenTextSplitter(150, 150, 50, 100, true); // from ChatGPT
        List<Document> documents = splitter.split(textReader.read()); // textReader will read the text file, splitter will split the text. Splitter will convert into List of Documents
        vectorStore.add(documents);
    }
}
