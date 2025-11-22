package com.example.SpringAIDemo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class SpringAiDemoApplication {

	public static void main(String[] args) {
		SpringApplication.run(SpringAiDemoApplication.class, args);
		// next step is to talk to the AI model
		// we do it with RestClient
		// Postman to send request
		// create a Controller

		// Go to Postman --> Get request --> http://localhost:8080/
		// Output: Hello World!!!!!!

		// GET http://localhost:8080/api/greet --> changed path

		// App -----> OpenAI (SpringAI uses something called as 'ChatModel' to connect with OpenAI)
		//For OpenAI, it will be OpenAI chatmodel, for Anthropic, it will be Anthropic chatmodel

		// Output from ChatModel

		/*
		Sure! Here’s a friendly greeting message you can use:
		---

🌟 		Hello and welcome! We're so glad to have you here. If you have any questions or need assistance, feel free to ask. Enjoy your time!

		---
		Feel free to customize it to better fit your style or audience!
		 */

		// Next we need Abstraction --> if model changes, we got to change the code
		// that means we got to remove the dependency
		// ChatClient is the way to go
		// APP --> ChatClient --> ChatModel --> OpenAI
		// App will talk to ChatClient then ChatClient talks to ChatModel. with ChatClient, we have more control. you get more data from ChatClient like Output, metadata (which model, what's the total token usage etc)
		// instead of ChatModel, we will use ChatClient

		// GET http://localhost:8080/api/chatclient/greet

		/*
		Sure! Here’s a friendly greeting message you can use:

		---

🌟 		Hello and welcome! We're so glad to have you here. If you have any questions or need assistance, feel free to reach out. Enjoy your time!

		---

		Feel free to customize it to better fit your style!
		 */


		// GET http://localhost:8080/api/chatclient/input/what's the best space movie ever?

		/*
		Determining the "best" space movie can be subjective and often depends on personal taste, genre preference, and the criteria used for evaluation. However, several films are frequently cited as some of the greatest in the genre:

		1. **2001: A Space Odyssey (1968)** - Directed by Stanley Kubrick, this film is renowned for its groundbreaking visual effects and philosophical themes. It explores human evolution, artificial intelligence, and the unknown.

		2. **Interstellar (2014)** - Directed by Christopher Nolan, this film combines science fiction with emotional storytelling, focusing on space exploration and the bond between a father and daughter.

		3. **The Martian (2015)** - Directed by Ridley Scott and based on Andy Weir's novel, it tells the story of an astronaut stranded on Mars and his struggle for survival, highlighting human ingenuity and resilience.

		4. **Gravity (2013)** - Directed by Alfonso Cuarón, this visually stunning film focuses on the survival of astronauts in space after their shuttle is destroyed. It’s praised for its technical achievements and emotional depth.

		5. **Alien (1979)** - Directed by Ridley Scott, this film blends horror and science fiction, featuring a crew that encounters a deadly extraterrestrial creature. It’s iconic for its atmosphere and strong female lead.

		6. **Blade Runner (1982)** - While more of a sci-fi noir, it explores themes of humanity and artificial intelligence in a dystopian future, and is highly regarded for its visuals and storytelling.

		Ultimately, the "best" space movie can vary widely based on individual preferences, but these films are often considered among the top in the genre.

		 */

	}


}
