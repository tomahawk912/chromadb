# Initialize client
### In-memory chroma
import chromadb

client = chromadb.Client()

### In-memory chroma with saving/loading to disk
# 이 모드에서 크로마는 세션 간에 데이터를 유지합니다. 로드 시 - 사용자가 지정한 디렉터리에 데이터를 로드합니다.
# 그리고 데이터를 추가하면 해당 디렉터리에 저장됩니다.
import chromadb

# client = chromadb.PersistentClient(path="/path/to/data")
client = chromadb.PersistentClient(path="D:\\Ptest\\2.chromadb\\chromadb")

### 크로마를 클라이언트로 실행하여 백엔드 서비스와 대화하기
import chromadb

chroma_client = chromadb.HttpClient(host="localhost", port=8000)

### Methods on Client
# Collection은 REST API의 URL에 사용되기 때문에 명명 요구 사항에서 AWS s3 버킷과 유사합니다.

# list all collections
client.list_collections()

# make a new collection
collection = client.create_collection("test_collection")

# get an existing collection
collection = client.get_collection("test_collection")

# get a collection or create if it doesn't exist already
collection = client.get_or_create_collection("test_collection")

# delete a collection
client.delete_collection("test_collection")


### Utility methods ###################################################
# resets entire database - this *cant* be undone!
client.reset()

# returns timestamp to check if service is up
client.heartbeat()


### Metods on Collection ##################################################

# change the name or metadata on a collection
collection.modify(name="testname2")

# get the number of items in a collection
collection.count()

# add new items to a collection
# either one at a time
collection.add(
    embeddings=[1.5, 2.9, 3.4],
    metadatas={"uri": "img9.png", "style": "style1"},
    documents="doc1000101",
    ids="uri9",
)
# or many, up to 100k+!
collection.add(
    embeddings=[[1.5, 2.9, 3.4], [9.8, 2.3, 2.9]],
    metadatas=[{"style": "style1"}, {"style": "style2"}],
    ids=["uri10", "uri11"],
)
# 기본 임베딩 (384차원)으로 입력됨
client.delete_collection("test_collection")
collection = client.create_collection("test_collection")
collection.add(
    documents=["doc1000101", "doc288822"],
    metadatas=[{"style": "style1"}, {"style": "style2"}],
    ids=["uri12", "uri13"],
)

# update items in a collection
collection.update()

# upsert items. new items will be added, existing items will be updated.
collection.upsert(
    ids=["id1", "id2", "id3", ...],
    embeddings=[[1.1, 2.3, 3.2], [4.5, 6.9, 4.4], [1.1, 2.3, 3.2], ...],
    metadatas=[
        {"chapter": "3", "verse": "16"},
        {"chapter": "3", "verse": "5"},
        {"chapter": "29", "verse": "11"},
        ...,
    ],
    documents=["doc1", "doc2", "doc3", ...],
)

collection.get(include=["documents", "embeddings", "metadatas"], ids=["id2"])

# get items from a collection
collection.get()

# convenience, get first 5 items from a collection
collection.peek()

# do nearest neighbor search to find similar embeddings or documents, supports filtering
collection = client.get_collection("tab_tree912")
collection.query(
    query_embeddings=[[1.1, 2.3, 3.2], [5.1, 4.3, 2.2]],
    n_results=2,
    where={"style": "style2"},
)

# delete items
collection.delete()
