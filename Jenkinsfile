pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    component: ci
spec:
  serviceAccount: jenkins
  containers:
  - name: docker
    image: docker
    command:
    - cat
    tty: true
    volumeMounts:
    - name: dockerd
      mountPath: /var/run/docker.sock
  volumes:
  - name: dockerd
    hostPath:
      path: /var/run/docker.sock
"""
        }
    }
    stages {
        stage("Build") {
            steps {
                container("docker") {
                    sh("docker build -t md-notifications .")
                }
            }
        }
    }
}