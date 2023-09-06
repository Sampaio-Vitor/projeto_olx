# `README.md`
Acesse o site [apepreve.lat](https://apepreve.lat) por aqui!
---
# INTERFACE DO PROJETO:

![image](https://github.com/Sampaio-Vitor/projeto_olx/assets/110466124/5b214661-82a6-4186-bb91-48fb5c4f33af)


## **ApêPrevê: Predição de Preços de Imóveis na OLX**

**Status:** 🚧 Em Andamento 🚧

### **Visão Geral:**
Este projeto tem como objetivo realizar raspagem de dados (web scraping) diária na OLX, aplicar algoritmos de aprendizado de máquina aos dados coletados e informar ao usuário se, de acordo com as previsões do algoritmo, o preço do anúncio está baixo ou alto. Em resumo, ele ajudará os usuários a identificar se uma negociação de imóvel é vantajosa ou não.

### **Arquitetura e Fluxo de Trabalho:**
1. **Web Scraping:** Scripts automatizados de raspagem de dados coletarão diariamente informações sobre imóveis na OLX. Utilizado Selenium e BeautifulSoup, rodando em uma instancia EC2 através de um container Docker.
2. **Engenharia de Dados:** Pipelines de ingestão de dados limparão, transformarão e enriquecerão os dados brutos. Realizado o básico, dados gravados em csv's no S3.
3. **Aprendizado de Máquina:** Modelo de predição (RandomForestRegressor) treinado para realizar previsões baseadas nos dados coletados.
4. **MLOps:** Utilizado Docker em conjunto com Github Actions e ECR para esteira CI/CD. Retreinamento automatico do modelo será implementado, além de atualização diária das métricas em um arquivo MD.
5. **Interface do Usuário:** Desenvolvida uma interface que fornecerá aos usuários insights sobre o mercado imobiliário, destacando possíveis bons negócios.

### **Próximas implementações:**
1. Adicionar logging ao código para que tenhamos controle maior sob o que ocorre por trás e registra-los em um arquivo de log;
2. Reorganizar código removendo partes que possivelmente sejam inuteis.
3. Criar calculadora que solicitará o usuário os detalhes do apartamento, e através de solicitação API para o modelo treinado, será retornado o valor sugerido para o apartamento.
4. Criar dashboard dos dados entrantes, com georeferenciamento.
5. Criar arquivo MD que explica cada função utilizada no código.
6. Implementar certificado SSL no website.
7. Salvar os dados em um banco de dados SQL na AWS, invés de CSV no S3.


### **Stack:**

- **Ambiente em Nuvem:** Amazon Web Services (AWS)
- **Armazenamento de Dados:** S3 AWS (tanto para dados brutos no data lake quanto para dados processados após previsões de ML)
- **MLOps:** GitHub Actions para automação CI/CD e retreino de modelos
- **Backend & API:** Flask + S3
- **Frontend:** Painel Web (Flask, HTML e CSS)


### **Contribuições:**

Este projeto está na fase ativa de desenvolvimento. Se você está interessado em contribuir ou tem sugestões, crie um problema ou envie um pull request.

---

*Última Atualização: *06/09/2023*


