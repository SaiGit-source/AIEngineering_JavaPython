## https://platform.openai.com/docs/guides/embeddings/embedding-models?lang=python

from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables from .env.

api_key = os.getenv("OPENAI_API_KEY")


from openai import OpenAI
client = OpenAI()

words = ["Dog", "Cat", "Apple", "Orange", "Car", "Bus", "Tree", "Flower", "Computer", "Phone"]

for word in words:
    response = client.embeddings.create(
        input=word,
        model="text-embedding-3-small"
        dimensions=2
    )
    print(f"Word: {word}")
    print(response.data[0].embedding)
    print(len(response.data[0].embedding))
    print("\n")
    
    
response = client.embeddings.create(
    input="Dog",
    model="text-embedding-3-small",
    dimensions=2
)

print(response.data[0].embedding)
print(len(response.data[0].embedding))
embedding = response.data[0].embedding
print(f"{word} = ({embedding[0]:.6f}, {embedding[1]:.6f})")


### Output
### [3911008835, 0.00890826154500246, 0.004556112922728062, 0.012535511516034603, -0.017695248126983643, 0.02388031594455242, -0.01897415705025196, -0.04970104247331619, 0.02703348733484745, -0.01760704629123211, -0.009812317788600922, -0.017794473096728325, 0.030054358765482903, 0.010799062438309193, 0.012072458863258362, 0.0010666761081665754, -0.01705579273402691, 0.023549562320113182, 0.027518590912222862, 0.015291781164705753, 0.0013202528934925795, 0.009498103521764278, 0.03905082121491432, -6.925126217538491e-05, 0.018191376700997353, -0.016416339203715324, 0.051950160413980484, 0.026129430159926414, -0.015931235626339912, 0.014751551672816277, ...]
### it printed 1536 dimensions
## 1536

## [0.9827378988265991, 0.1850033700466156]
##  2