# File Management System with Keycloak & MinIO & Docker
1. Setting up and Running the Project
   - clone the repository

2. Run docker
    - docker-compose up --build
    - docker-compose up -d
    - http://localhost:8000/
3. Setup .env
   - update .env file
     
4. Keycloak
   - login with admin/admin
   - open realm
   - open user and generate password
   - update .env
   - http://localhost:8080/
  
5. MiniIO
   - open miniIO
   - create access keys
   - http://localhost:9001/
  
6. Example zaqvki

curl -X POST http://127.0.0.1:8000/upload \
-H "Authorization: Bearer <JWT_TOKEN>" \
-F "file=@example.txt"


curl -X GET http://127.0.0.1:8000/download/<file_id> \
-H "Authorization: Bearer <JWT_TOKEN>" \
-o downloaded_file.txt


curl -X PUT http://127.0.0.1:8000/update/<file_id> \
-H "Authorization: Bearer <JWT_TOKEN>" \
-F "file=@updated_example.txt"


curl -X DELETE http://127.0.0.1:8000/delete/<file_id> \
-H "Authorization: Bearer <JWT_TOKEN>"


curl -X POST http://127.0.0.1:8080/realms/<REALM_NAME>/protocol/openid-connect/token \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "client_id=<CLIENT_ID>" \
-d "client_secret=<CLIENT_SECRET>" \
-d "username=<USERNAME>" \
-d "password=<PASSWORD>" \
-d "grant_type=password"

  
