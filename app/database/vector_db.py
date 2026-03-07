# import chromadb

# client = chromadb.Client(
#      chromadb.config.Settings(
#         persist_directory="./chroma_db"
#     )
# )

# collection = client.get_or_create_collection(name="image_search")

# def store_embedding(embedding , image_path):

#     collection.add(
#         embeddings=[embedding],
#         metadatas=[{"image":image_path}],
#         ids=[image_path]
#     )
#     client.persist()
#     print("done ")



import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(name="image_search")

def store_embedding(embedding, image_path):

    collection.add(
        embeddings=[embedding],
        metadatas=[{"image": image_path}],
        ids=[image_path]
    )

    print("stored successfully")