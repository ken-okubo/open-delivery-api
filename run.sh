#!/bin/bash

# Inicia o projeto usando Docker
echo "Iniciando Open Delivery API com Docker..."

# Constrói e inicia os contêineres
docker-compose up - d

echo ""
echo "API rodando em: http://localhost:8000"
echo "Documentação: http://localhost:8000/docs"
