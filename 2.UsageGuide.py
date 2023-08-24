
# 1. 영구 DB 생성

import chromadb

# 로컬 컴퓨터에서 저장하고 로드하도록 Chroma를 구성할 수 있습니다. 데이터는 자동으로 유지되며 시작 시 로드됩니다(데이터가 있는 경우).
client = chromadb.PersistentClient(path="D:\\Ptest\\2.chromadb\\chromadb")

# 한 번에 하나의 클라이언트만 사용
# 많은 클라이언트가 동일한 경로에 로드 및 저장하면 데이터 삭제 등 이상한 동작이 발생할 수 있습니다.
# 일반적으로 애플리케이션에서 한 번만 Chroma 클라이언트를 생성하고 여러 클라이언트를 생성하지 말고 전달하세요.

# 클라이언트 객체의 유용한 편의 메서드
client.heartbeat() # 나노초 단위의 하트비트를 반환. 클라이언트가 계속 연결되어 있는지 확인
client.reset() # 데이터베이스를 비우고 완전히 초기화. 되돌릴 수 없음

# 2. 클라이언트/서버 모드에서 크로마DB 실행
# 메모리를 초과하는 대용량 데이터에 유용한 온디스크 데이터베이스를 사용하도록 Chroma를 구성할 수도 있음
# 클라이언트 서버 모드에서 Chroma를 실행하도록 도커 컨테이너를 실행하세요
docker-compose up -d --build

# Python HTTP 전용 클라이언트 사용
# 클라이언트-서버 모드에서 크로마를 실행하는 경우.
# 전체 Chroma 라이브러리가 필요하지 않고 클라이언트 머신에 클라이언트 라이브러리만 필요할 수 있습니다.
# 이 경우 chromadb-client 패키지를 설치하면 됩니다. 이 패키지는 종속성 설치 공간을 최소화하는 서버용 경량 HTTP 클라이언트입니다.
pip install chromadb-client

import chromadb
from chromadb.config import Settings
# Example setup of the client to connect to your chroma server
client = chromadb.HttpClient(host='localhost', port=8000)

# 3. 컬렉션 사용

# 크로마에서는 컬렉션 Premitive를 사용하여 임베딩 컬렉션을 관리할 수 있습니다.

# 가. 컬렉션 만들기, 검사 및 삭제하기
#
# 컬렉션 만들기, 검사 및 삭제하기
# Chroma는 URL에서 컬렉션 이름을 사용하므로 컬렉션 이름 지정에 몇 가지 제한이 있습니다:
#
# - 이름의 길이는 3~63자 사이여야 합니다.
# - 이름은 소문자 또는 숫자로 시작하고 끝나야 하며 그 사이에 점, 대시, 밑줄을 포함할 수 있습니다.
# - 이름에 두 개의 연속된 점이 포함되어서는 안 됩니다.
# - 이름은 유효한 IP 주소가 아니어야 합니다.
# 크로마 컬렉션은 이름과 임베딩 함수(선택 사항)로 생성됩니다. 임베딩 함수를 제공하는 경우 컬렉션을 가져올 때마다 임베딩 함수를 제공해야 합니다.
collection = client.create_collection(name="my_collection", embedding_function=emb_fn)
collection = client.get_collection(name="my_collection", embedding_function=emb_fn)

# 주의) 나중에 get_collection을 사용하려면 컬렉션을 만들 때 제공한 임베딩 함수를 사용해야 합니다.
# 임베딩 함수는 텍스트를 입력으로 받아 토큰화 및 임베딩을 수행합니다. 임베딩 함수가 제공되지 않으면 Chroma는 Sentence Transformer를 기본값으로 사용합니다.
# 임베딩 함수 및 임베딩 함수를 직접 만드는 방법에 대해 자세히 알아보세요.
#
# 기존 컬렉션은 .get_collection을 사용하여 이름으로 검색하고 .delete_collection을 사용하여 삭제할 수 있습니다.
# 또한 .get_or_create_collection을 사용하여 컬렉션이 있는 경우 컬렉션을 가져오고, 없는 경우 컬렉션을 만들 수도 있습니다.

collection = client.get_collection(name="test") # 기존 컬렉션에서 이름으로 컬렉션 객체를 가져옵니다. 찾을 수 없으면 예외를 발생시킵니다.
collection = client.get_or_create_collection(name="test") # 기존 컬렉션에서 이름으로 컬렉션 객체를 가져옵니다. 존재하지 않는 경우 생성합니다.
client.delete_collection(name="my_collection") # 컬렉션과 관련된 모든 임베딩, 문서 및 메타데이터를 삭제합니다.

collection.peek() # 컬렉션의 처음 10개 항목 목록을 반환합니다.
collection.count() # 컬렉션의 항목 수를 반환합니다.
collection.modify(name="new_name") # 컬렉션 이름 바꾸기

# Distance 함수 변경
# create_collection은 선택적 메타데이터 인수를 받기도 하는데, 이 인수는 hnsw:space 값을 설정하여 임베딩 스페이스의 거리 메서드를 사용자 지정하는 데 사용할 수 있음

collection = client.create_collection(
    name="collection_name",
    metadata={"hnsw:space": "cosine"}  # l2 is the default
)
# hnsw:space에 유효한 옵션은 "l2", "ip" 또는 "코사인"입니다. 기본값은 "l2"입니다. 각 옵션에 대한 방정식은 여기 Hnswlib 문서에서 찾을 수 있음

# 컬렉션에 데이터 추가 : .add
collection.add(
    documents=["lorem ipsum...", "doc2", "doc3", ...],
    metadatas=[{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}, ...],
    ids=["id1", "id2", "id3", ...]
)
# 문서목록이 Chroma에 전달되면 컬렉션의 임베딩 기능을 사용하여 자동으로 토큰화하여 임베딩합니다(컬렉션 생성 시 제공된 문서가 없는 경우 기본값이 사용됨)
# Chroma는 문서 자체도 저장합니다. 문서가 너무 커서 선택한 임베딩 함수를 사용하여 임베드할 수 없는 경우 예외가 발생합니다.
# 각 문서에는 고유한 연관 ID가 있어야 합니다. 동일한 ID를 두 번 .add하려고 하면 초기 값만 저장됩니다.
# 추가 정보를 저장하고 필터링을 활성화하기 위해 각 문서에 대해 메타데이터 사전 목록을 선택적으로 제공할 수 있습니다.
# 또는 문서와 연관된 임베딩 목록을 직접 제공할 수 있으며, Chroma는 임베딩하지 않고 연관된 문서를 저장합니다.

collection.add(
    documents=["doc1", "doc2", "doc3", ...],
    embeddings=[[1.1, 2.3, 3.2], [4.5, 6.9, 4.4], [1.1, 2.3, 3.2], ...],
    metadatas=[{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}, ...],
    ids=["id1", "id2", "id3", ...]
)
# 제공된 임베딩이 컬렉션과 동일한 차원이 아닌 경우 예외가 발생합니다.
# 문서를 다른 곳에 저장하고 임베딩 목록과 메타데이터만 Chroma에 제공할 수도 있습니다. ID를 사용하여 임베딩을 다른 곳에 저장된 문서와 연결할 수 있습니다.

collection.add(
    embeddings=[[1.1, 2.3, 3.2], [4.5, 6.9, 4.4], [1.1, 2.3, 3.2], ...],
    metadatas=[{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}, ...],
    ids=["id1", "id2", "id3", ...]
)

# 컬렉션 조회 (Querying a Collection)
# 크로마 컬렉션은 .query 메서드를 사용하여 다양한 방법으로 쿼리할 수 있습니다.
# 쿼리_임베딩 집합으로 쿼리할 수 있습니다.
collection.query(
    query_embeddings=[[11.1, 12.1, 13.1],[1.1, 2.3, 3.2], ...],
    n_results=10,
    where={"metadata_field": "is_equal_to_this"}, #  메타데이터 필드가 "is_equal_to_this"와 같은 문서만 필터링
    where_document={"$contains":"search_string"} # 문서 내용에 "document"라는 단어가 포함된 문서만 필터링
)
# 쿼리는 각 쿼리 임베딩과 가장 일치하는 n_results를 순서대로 반환합니다.
# 선택적 where 필터 사전을 제공하여 각 문서와 연관된 메타데이터를 기준으로 결과를 필터링할 수 있습니다.
# 또한 선택적 where_document 필터 사전을 제공하여 문서의 내용을 기준으로 결과를 필터링할 수 있습니다.
# 제공된 쿼리_임베딩이 컬렉션과 동일한 차원이 아닌 경우 예외가 발생합니다.

# 쿼리_텍스트 집합으로 쿼리할 수도 있습니다.
# Chroma는 먼저 컬렉션의 임베딩 함수를 사용하여 각 쿼리 텍스트를 임베딩한 다음 생성된 임베딩으로 쿼리를 수행합니다.
collection.query(
    query_texts=["doc10", "thus spake zarathustra", ...],
    n_results=10,
    where={"metadata_field": "is_equal_to_this"},
    where_document={"$contains":"search_string"}
)

# .get을 사용하여 ID별로 컬렉션에서 항목을 검색할 수도 있습니다.
collection.get(
    ids=["id1", "id2", "id3", ...],
    where={"style": "style1"}
)

# 반환할 데이터 선택하기
# get 또는 쿼리를 사용할 때 include 매개변수를 사용하여 반환할 데이터(임베딩, 문서, 메타데이터, 쿼리의 경우 거리 중 하나)를 지정할 수 있습니다.
# 기본적으로 Chroma는 문서, 메타데이터, 쿼리의 경우 결과의 거리를 반환합니다. 임베딩은 성능을 위해 기본적으로 제외되며 ID는 항상 반환됩니다.
# 쿼리 또는 get 메서드의 includes 매개변수에 포함된 필드 이름의 배열을 전달하여 이 중 어떤 것을 반환할지 지정할 수 있습니다.
# Only get documents and ids
collection.get(
    include=["documents"]
)
collection.query(
    query_embeddings=[[11.1, 12.1, 13.1],[1.1, 2.3, 3.2], ...],
    include=["documents"]
)

# Where 조건 사용
# Chroma는 메타데이터와 문서 콘텐츠별로 쿼리를 필터링할 수 있습니다.
# where 필터는 메타데이터를 기준으로 필터링하는 데 사용되며, where_document 필터는 문서 콘텐츠를 기준으로 필터링하는 데 사용됩니다.

# 메타데이터로 필터링하기
# 메타데이터를 기준으로 필터링하려면 쿼리에 where 필터 사전을 제공해야 합니다. 사전은 다음과 같은 구조를 가져야 합니다:

{
    "metadata_field": {
        <Operator>: <Value>
    }
}
# 필터링 기호 : $eq - equal to (string, int, float), $ne - not equal to (string, int, float), $gt - greater than (int, float)
# $gte - greater than or equal to (int, float), $lt - less than (int, float), $lte - less than or equal to (int, float)

# $eq 사용 예시
{
    "metadata_field": "search_string"
}

# is equivalent to
{
    "metadata_field": {
        "$eq": "search_string"
    }
}

# 문서 내용으로 검색
# 문서 내용을 기준으로 필터링하려면 쿼리에 where_document 필터 딕셔너리를 제공해야 합니다. 딕셔너리는 다음과 같은 구조를 가져야 합니다:
# Filtering for a search_string
{
    "$contains": "search_string"
}

# 논리 연산자
# 논리 연산자 $and 및 $or를 사용하여 여러 필터를 결합할 수도 있습니다.

# $and 연산자는 목록에 있는 모든 필터와 일치하는 결과를 반환합니다.
{
    "$and": [
        {
            "metadata_field": {
                <Operator>: <Value>
            }
        },
        {
            "metadata_field": {
                <Operator>: <Value>
            }
        }
    ]
}
# $or 연산자는 목록의 필터와 일치하는 결과를 반환합니다.
{
    "$or": [
        {
            "metadata_field": {
                <Operator>: <Value>
            }
        },
        {
            "metadata_field": {
                <Operator>: <Value>
            }
        }
    ]
}

# Update 데이터
# 컬렉션에 있는 항목의 모든 속성은 .update를 사용하여 업데이트할 수 있습니다.
# id 조건으로 검색 후 Update
collection.update(
    ids=["id1", "id2", "id3", ...],
    embeddings=[[1.1, 2.3, 3.2], [4.5, 6.9, 4.4], [1.1, 2.3, 3.2], ...],
    metadatas=[{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}, ...],
    documents=["doc1", "doc2", "doc3", ...],
)
# 컬렉션에서 ID를 찾을 수 없는 경우 오류가 기록되고 업데이트가 무시됩니다. 해당 임베딩 없이 문서가 제공되면 컬렉션의 임베딩 기능으로 임베딩이 다시 수집됩니다.
# 제공된 임베딩이 컬렉션과 동일한 차원이 아닌 경우 예외가 발생합니다.

# Upsert : 크로마는 기존 항목을 업데이트하거나 아직 존재하지 않는 경우 추가하는 업서트 작업도 지원합니다.
collection.upsert(
    ids=["id1", "id2", "id3", ...],
    embeddings=[[1.1, 2.3, 3.2], [4.5, 6.9, 4.4], [1.1, 2.3, 3.2], ...],
    metadatas=[{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}, ...],
    documents=["doc1", "doc2", "doc3", ...],
)
# 컬렉션에 아이디가 없는 경우 추가에 따라 해당 항목이 생성됩니다. 기존 ID가 있는 항목은 업데이트에 따라 업데이트됩니다.

## Delete
# Chroma는 .delete를 사용하여 ID별로 컬렉션에서 항목 삭제를 지원합니다.
# 각 항목과 연결된 임베딩, 문서 및 메타데이터가 삭제됩니다.
# .delete는 where 필터도 지원합니다. ID가 제공되지 않으면 컬렉션에서 where 필터와 일치하는 모든 항목을 삭제합니다.
collection.delete(
    ids=["id1", "id2", "id3",...],
    where={"chapter": "20"}
)

# Authentication (인증)
# 서버/클라이언트 모드에 있을 때만 인증을 사용하도록 Chroma를 구성할 수 있습니다.
# 기본 인증방법
# 가. 서버 설정
# 서버 측 자격증명 생성
# 보안 관행
# 비밀번호를 안전하게 저장하는 것이 좋은 보안 관행입니다. 아래 예에서는 일반 텍스트 비밀번호를 해싱하기 위해 bcrypt(현재 Chroma 서버 측 인증에서 유일하게 지원되는 해시)를 사용합니다.
docker run --rm --entrypoint htpasswd httpd:2 -Bbn admin admin > server.htpasswd

# 서버 실행
# 다음 내용으로 .chroma_env 파일을 생성합니다:
# .chroma_env 파일
CHROMA_SERVER_AUTH_CREDENTIALS_FILE="/chroma/server.htpasswd"
CHROMA_SERVER_AUTH_CREDENTIALS_PROVIDER='chromadb.auth.providers.HtpasswdFileServerAuthCredentialsProvider'
CHROMA_SERVER_AUTH_PROVIDER='chromadb.auth.basic.BasicAuthServerProvider'

docker-compose --env-file ./.chroma_env up -d --build

# 나. 클라이언트 설정
import chromadb
from chromadb.config import Settings

client = chromadb.HttpClient(
  settings=Settings(chroma_client_auth_provider="chromadb.auth.basic.BasicAuthClientProvider",chroma_client_auth_credentials="admin:admin"))
client.heartbeat()  # this should work with or without authentication - it is a public endpoint

client.get_version()  # this should work with or without authentication - it is a public endpoint

client.list_collections()  # this is a protected endpoint and requires authentication



############################# 실습 : 임의 임베딩 (임베딩 함수 미사용)
from pprint import pprint
import chromadb

# DB 생성
client = chromadb.PersistentClient(path="D:\\Ptest\\2.chromadb\\chromadb")
client.delete_collection(name="my_collection")
collection = client.create_collection(name="tab_tree912")
collection.add(
    embeddings=[[1.9, 2.5, 4.5], [6.7, 8.2, 9.2]],
    documents=["This is a document", "This is another document"],
    metadatas=[{"source": "my_source"}, {"source": "my_source"}],
    ids=["kd1", "kd2"]
)
collection = client.get_collection(name="tab_tree912")
collection.count()
pprint(collection.peek())

# {'documents': ['This is a document',
#                'This is another document',
#                'This is a document',
#                'This is another document'],
#  'embeddings': [[1.2000000476837158, 2.299999952316284, 4.5],
#                 [6.699999809265137, 8.199999809265137, 9.199999809265137],
#                 [1.2000000476837158, 2.299999952316284, 4.5],
#                 [6.699999809265137, 8.199999809265137, 9.199999809265137]],
#  'ids': ['id1', 'id2', 'kd1', 'kd2'],
#  'metadatas': [{'source': 'my_source'},
#                {'source': 'my_source'},
#                {'source': 'my_source'},
#                {'source': 'my_source'}]}

# 임베딩 벡터로 조회
pprint(collection.query(
    query_embeddings=[6.7, 8.2, 9.2],
    n_results=1,
    where={"source": "my_source"},
    where_document={"$contains":"another"}
))

# 텍스트로 조회 (Default 임베딩 함수 사용으로 인한 오류발생)
pprint(collection.query(
    query_texts=["This is the other document"],
    n_results=1,
    where={"source": "my_source"},
    where_document={"$contains":"another"}
))

# id로 조회
pprint(collection.get(
    include=["documents","embeddings","metadatas"],
    ids=["id2"]
))

# id로 조회 후 메타데이터 업데이트
collection.update(
    ids=["id2","kd2"],
    metadatas=[{'source':'your_source'},{'source':'your_source'}],
)
pprint(collection.peek())
collection.count()
