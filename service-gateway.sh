#!/bin/bash
kubectl delete deployment generate 
kubectl delete deployment populate
kubectl delete deployment retrieve
kubectl delete deployment gateway
./build.sh
sleep 10
minikube service gateway --url