sudo docker stop backend
sudo docker rm backend
sudo docker rmi resitasriw/backend
sudo docker run -d --name backend -p 3000:80 resitasriw/backend:latest
