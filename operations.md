# kubernetes/gcloud commands

## docker hub login
gcloud docker login

## store secret
kubectl create secret generic ssh-key-secret --from-file=ssh-privatekey=$HOME/.ssh/id_rsa --from-file=ssh-publickey=$HOME/.ssh/id_rsa.pub

## build docker image
docker build -t gcr.io/thesecretaryofwar/python:v1 .

## push docker image
gcloud docker push gcr.io/thesecretaryofwar/python:v1

## create cluster
gcloud container clusters create wikidiff --num-nodes=1 --disk-size=250 --zone=us-east1-b --machine-type=n1-highmem-2

## delete cluster
gcloud container clusters delete wikidiff

## register cluster
gcloud container clusters get-credentials wikidiff

## start a job/pod
kubectl create -f ./NAME.yaml

## delete a job/pod
kubectl delete -f ./NAME.yaml
kubectl delete pods/NAME
kubectl delete jobs/NAME

## list pods
kubectl get pods -a

## get logs
kubectl logs POD_NAME
