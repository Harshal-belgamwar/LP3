
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


with open("document1.txt", "r", encoding="utf-8") as f:
    text1 = f.read()

with open("document2.txt", "r", encoding="utf-8") as f:
    text2 = f.read()


vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform([text1, text2])


similarity = cosine_similarity(vectors[0], vectors[1])[0][0]


print("Document 1:", text1)
print("Document 2:", text2)
print(f"\nSimilarity Score: {similarity:.4f}")
print(f"Similarity Percentage: {similarity * 100:.2f}%")
