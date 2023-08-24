# 1.Install : pip install chromadb

# 2.Get the Chroma Client
import chromadb
chroma_client = chromadb.Client()

# 3.Create a collection
collection = chroma_client.create_collection(name="my_collection")

# 4.Add some text documents to the collection
# Chroma는 텍스트를 저장하고 토큰화, 임베딩, 인덱싱을 자동으로 처리합니다.
collection.add(
    documents=["This is a document", "This is another document"],
    metadatas=[{"source": "my_source"}, {"source": "my_source"}],
    ids=["id1", "id2"]
)

# 이미 임베딩을 직접 생성한 경우 바로 불러올 수 있습니다:
collection.add(
    embeddings=[[1.2, 2.3, 4.5], [6.7, 8.2, 9.2]],
    documents=["This is a document", "This is another document"],
    metadatas=[{"source": "my_source"}, {"source": "my_source"}],
    ids=["id1", "id2"]
)

# 5. Query the collection
# 쿼리 텍스트 목록으로 컬렉션을 쿼리할 수 있으며, Chroma는 가장 유사한 n개의 결과를 반환합니다. 정말 간단합니다!
results = collection.query(
    query_texts=["This is a query document"],
    n_results=2
)
print(results)