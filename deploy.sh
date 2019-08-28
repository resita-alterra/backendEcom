sudo docker stop backend
sudo docker rm backend
sudo docker rmi resitasriw/backend
sudo docker run -d --name backend -p 5000:5000 resitasriw/backend:latest
