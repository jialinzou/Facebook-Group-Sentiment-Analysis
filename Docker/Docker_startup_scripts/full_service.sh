cd ../../ && sudo docker build --file="Docker/Dockerfiles/Dockerfile" -t mxlei01/facebook-sentiment-analysis .
sudo docker run --net="host" --name facebook-sentiment-analysis mxlei01/facebook-sentiment-analysis &
sleep 15 && sudo docker exec -i -t facebook-sentiment-analysis bash
