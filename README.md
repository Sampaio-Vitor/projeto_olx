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
1. **Web Scraping:** Scripts automatizados de raspagem de dados coletarão diariamente informações sobre imóveis na OLX.
2. **Engenharia de Dados:** Pipelines de ingestão de dados limparão, transformarão e enriquecerão os dados brutos. Realizado o básico, dados gravados em csv's no S3
3. **Aprendizado de Máquina:** Um modelo de predição será treinado para determinar se os preços dos imóveis estão altos ou baixos com base em dados históricos e novos.
4. **MLOps:** Usando GitHub Actions, o modelo será retreinado quinzenalmente. O modelo de melhor desempenho será selecionado automaticamente. Relatórios sobre as métricas do modelo serão mantidos e atualizados em um arquivo dedicado `report.md`.
5. **Interface do Usuário:** Desenvolvida uma interface fornecerá aos usuários insights sobre o mercado imobiliário, destacando possíveis bons negócios.

### **Stack:**

- **Ambiente em Nuvem:** Amazon Web Services (AWS)
- **Armazenamento de Dados:** S3 AWS (tanto para dados brutos no data lake quanto para dados processados após previsões de ML)
- **MLOps:** GitHub Actions para automação CI/CD e retreino de modelos
- **Backend & API:** Flask + S3
- **Frontend:** Painel Web


### **Contribuições:**

Este projeto está na fase ativa de desenvolvimento. Se você está interessado em contribuir ou tem sugestões, crie um problema ou envie um pull request.

---

*Última Atualização: *06/09/2023*


