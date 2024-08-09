# 🎉 Welcome to Productivity Rate k8s! 🎉

aws eks update-kubeconfig --region eu-north-1 --name ex-eks
kubectl taint node <node-name> CriticalAddonsOnly=true:NoSchedule-

kubectl apply -f .
kubectl delete -f .

kubectl patch storageclass gp2 -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
