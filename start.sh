docker build --no-cache -t booking_server_bot .
docker run -dp 8001:8001 --name booking_server_container booking_server_bot