cd ../../ && sudo docker build --file="Docker/Dockerfiles/Dockerfile" -t mxlei01/facebook-sentiment-analysis .
sudo docker run --net="host" --name facebook-sentiment-analysis mxlei01/facebook-sentiment-analysis &
cd ./Docker/Nginx && sudo docker build --file="Dockerfile" -t mxlei01/mxlei01-nginx .
sudo docker run --net="host" --name mxlei01-nginx mxlei01/mxlei01-nginx &
sleep 60 && sudo docker exec -i -t facebook-sentiment-analysis bash
