# remove old containers from all nodes

for node in $(kubectl get nodes -o json | jq -r '.items[].metadata.name')
do
    echo $node
    gcloud compute --project "thesecretaryofwar" ssh --zone "us-east1-b" "$node" --command="docker rm \$(docker ps -q -f status=exited)"
done
