echo "Pulizia immagini minikube"
minikube image list | grep rag- | xargs minikube image rm

cd gateway
docker images --format "{{.Repository}}:{{.Tag}}" | grep "rag-gateway" | xargs docker rmi
echo "Inizio la build di gateway"
docker build --no-cache -t rag-gateway:latest .

echo "Pusho gateway in minikube"
minikube image load rag-gateway:latest
                    
cd ../retrieve
docker images --format "{{.Repository}}:{{.Tag}}" | grep "rag-retrieve" | xargs docker rmi
echo "Inizio la build di retrieve"
docker build --no-cache -t rag-retrieve:latest .
echo "Pusho retrieve in minikube"
minikube image load rag-retrieve:latest   
    
cd ../populate
docker images --format "{{.Repository}}:{{.Tag}}" | grep "rag-populate" | xargs docker rmi
echo "Inizio la build di populate"
docker build --no-cache -t rag-populate:latest .
echo "Pusho populate in minikube"
minikube image load rag-populate:latest
      
cd ../generate
docker images --format "{{.Repository}}:{{.Tag}}" | grep "rag-generate" | xargs docker rmi
echo "Inizio la build di generate"
docker build --no-cache -t rag-generate:latest .
echo "Pusho generate in minikube"
minikube image load rag-generate:latest

minikube image list | grep rag-
minikube image list | grep chroma

cd ../retrieve
kubectl apply -f kubernetes/
echo "Kubernetes apply retrieve" 

cd ../gateway
kubectl apply -f kubernetes/
echo "Kubernetes apply gateway"   

cd ../populate
kubectl apply -f kubernetes/
echo "Kubernetes apply populate"  

cd ../generate
kubectl apply -f kubernetes/
echo "Kubernetes apply generate"    