Setup

Create a local certificate to run https locally  
`brew install mkcert nss`  
`mkcert localhost 127.0.0.1`    

Run local webapp, database, and nginx containers  
`docker-compose up`

Navigate to app  
https://localhost/ or https://127.0.0.1/
