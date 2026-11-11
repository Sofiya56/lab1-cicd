# Task Manager - Kubernetes + Helm

Розподілений застосунок для керування завданнями: односторінковий клієнт (nginx), REST API (FastAPI, SQLAlchemy), PostgreSQL та окремий застосунок міграцій (Alembic).

## Компоненти

| Компонент | Образ |
|---|---|
| API | sofiya56/lab4-api |
| Клієнт | sofiya56/lab4-client |
| Міграції (Job) | sofiya56/lab4-migrator |
| База даних | postgres:16 (StatefulSet + PV/PVC/StorageClass) |

Ingress спрямовує `/api` до API, а `/` до клієнта.

## Як упакувати Helm Chart

    helm lint k8s/webapp
    helm package k8s/webapp --destination dist

У CI це робить job `helm-package`; архів `.tgz` зберігається в артефактах запуску GitHub Actions.

## Як встановити

Потрібні кластер Kubernetes (kind) та NGINX Ingress Controller.

    helm upgrade --install lab k8s/webapp -n webapp-lab --create-namespace --wait --wait-for-jobs --timeout 10m
    kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8080:80

Додайте у файл hosts запис `127.0.0.1 webapp.lab.test` і відкрийте http://webapp.lab.test:8080

Параметри (образи, порти, БД, Ingress) задаються у `k8s/webapp/values.yaml`.

## Видалення

    helm uninstall lab -n webapp-lab

## CI

GitHub Actions: збірка і тести, Docker-образи (api, client, migrator) у Docker Hub, пакування Helm Chart.