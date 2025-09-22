from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
documents = [
    "The new features in this update are amazing!",
    "I am really disappointed with the customer service, the features are bad.",
    "The amazing customer service helped me resolve my issues quickly.",
    "This is the best update yet, I love the new look and features.",
]
vectorizer = TfidfVectorizer(stop_words = 'english')

trfidf_matrix = vectorizer.fit_transform(documents)

feature_names = vectorizer.get_feature_names_out()

first_document_vector = trfidf_matrix[0]

df = pd.DataFrame(first_document_vector.T.todense(),index = feature_names, columns = ["tfidf"])
df = df.sort_values(by=["tfidf"], ascending=False)
print("--- Top keywords for the first comment ---")
print(df.head(5))