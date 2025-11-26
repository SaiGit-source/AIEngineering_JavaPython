package com.example.SpringAIDemo.moviereco;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.ai.chat.prompt.PromptTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
public class moviecontroller {
    // to get Metadata and other extra contents

    private ChatClient chatClient;
    public moviecontroller(ChatClient.Builder builder){
        this.chatClient = builder.build();
    }

    /*
    Other point is formatting the output. When we wanted movie recommendation, we were sending some request and getting some output
What if you want the output in the proper format? Thats where we could use something called as a 'Prompt Template'. you can create a Prompt Template, basically a String
We can have some pre-defined stuff and add user-text and you can display data in a particular format
     */

    // here i have specified what language i want movie in, which year i want the movie from or type of movie
    @GetMapping("/api/movie")
    public String getMovie(@RequestParam String type, @RequestParam String year, @RequestParam String lang){
        String promptStr = """
                i want to watch a {type} movie with good rating,
                released around {year} in {lang} language.
                Suggest one specific movie and tell me the cast and length of the movie.
                """;

        PromptTemplate template = PromptTemplate.builder()
                .template(promptStr)
                .build();
        Prompt prompt = template.create(Map.of("type", type, "year", year, "lang", lang)); // dynamically replacing the variables in the prompt string
        // now our prompt is ready

        String result = chatClient
                .prompt(prompt)
                .call()
                .content();
        return result;
    }

    // Output
    // GET http://localhost:8080/api/movie/?type=Comedy&year=2020&lang=English
/*
I recommend watching the comedy movie **"Palm Springs"** released in 2020. It has received positive reviews for its clever take on the romantic comedy genre.

**Cast:**
- Andy Samberg as Nyles
- Cristin Milioti as Sarah Wilder
- J.K. Simmons as Roy
- Peter Gallagher as Howard Wilder
- Meredith Hagner as Misty

**Length:** The movie has a runtime of approximately 90 minutes.
 */

    // i am customizing response
    @GetMapping("/api/movie/custom/")
    public String getMovie1(@RequestParam String type, @RequestParam String year, @RequestParam String lang){
        String promptStr = """
                i want to watch a {type} movie with good rating,
                released around {year} in {lang} language.
                Suggest one specific movie and tell me the cast and length of the movie.
                
                response format should be:
                Movie Name : <name>
                Cast : <cast>
                Length : <length>
                IMDB rating : <rating>
                <Basic Plot> : <plot>
                """;

        PromptTemplate template = PromptTemplate.builder()
                .template(promptStr)
                .build();
        Prompt prompt = template.create(Map.of("type", type, "year", year, "lang", lang)); // dynamically replacing the variables in the prompt string
        // now our prompt is ready

        String result = chatClient
                .prompt(prompt)
                .call()
                .content();
        return result;
    }
// Output
    // GET http://localhost:8080/api/movie/custom/?type=Comedy&year=2020&lang=English
    /*
    Movie Name: Palm Springs
Cast: Andy Samberg, Cristin Milioti, J.K. Simmons, Peter Gallagher
Length: 90 minutes
IMDB rating: 7.4/10
Basic Plot: "Palm Springs" follows the story of Nyles and Sarah, who meet at a wedding in the desert. When they get stuck in a time loop, they are forced to relive the same day over and over again. As they navigate this strange and comedic situation, they grow closer and explore the possibilities of love and life.
     */
}


