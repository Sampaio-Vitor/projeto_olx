# `README.md`

---
# MVP DO PROJETO:

![image](https://github.com/Sampaio-Vitor/projeto_olx/assets/110466124/abfe3647-0d04-44f6-9558-d51a660809e2)


## **Projeto: Predição de Preços de Imóveis na OLX**

**Status:** 🚧 Em Andamento 🚧

### **Visão Geral:**
Este projeto tem como objetivo realizar raspagem de dados (web scraping) diária na OLX, aplicar algoritmos de aprendizado de máquina aos dados coletados e informar ao usuário se, de acordo com as previsões do algoritmo, o preço do anúncio está baixo ou alto. Em resumo, ele ajudará os usuários a identificar se uma negociação de imóvel é vantajosa ou não.

### **Arquitetura e Fluxo de Trabalho:**
1. **Web Scraping:** Scripts automatizados de raspagem de dados coletarão diariamente informações sobre imóveis na OLX.
2. **Engenharia de Dados:** Pipelines de ingestão de dados limparão, transformarão e enriquecerão os dados brutos. Estamos utilizando a ferramenta "Great Expectations" para validação de dados e verificações de qualidade.
3. **Aprendizado de Máquina:** Um modelo de predição será treinado para determinar se os preços dos imóveis estão altos ou baixos com base em dados históricos e novos.
4. **MLOps:** Usando GitHub Actions, o modelo será retreinado diariamente. O modelo de melhor desempenho será selecionado automaticamente. Relatórios sobre as métricas do modelo serão mantidos e atualizados em um arquivo dedicado `report.md`.
5. **Interface do Usuário:** Uma interface (ainda a ser projetada) fornecerá aos usuários insights sobre o mercado imobiliário, destacando possíveis bons negócios.

### **Stack:**

- **Ambiente em Nuvem:** Amazon Web Services (AWS)
- **Armazenamento de Dados:** Google Cloud Storage (tanto para dados brutos no data lake quanto para dados processados após previsões de ML)
- **MLOps:** GitHub Actions para automação CI/CD e retreino de modelos
- **Validação de Dados:** Great Expectations
- **(Potencial) Backend & API:** GCP Functions, Cloud Run ou App Engine (Detalhes a serem finalizados)
- **(Potencial) Frontend:** Painel Web (Detalhes a serem finalizados)

### **Próximos Passos:**

- [✅] Treinar os modelos iniciais e definir benchmarks para as métricas do modelo.
- [✅] Configurar pipelines de ingestão de dados usando Apache Beam e garantir a validação de dados usando o Great Expectations.
- [✅] Configurar o GitHub Actions para o fluxo de trabalho MLOps.
- [✅] Projetar e implementar a interface do usuário.
- [ ] Dockerizar a aplicação e colocar na nuvem em uma instância EC2 (AWS).
- [ ] Aplicar tratativas de MLOps (GitHub Actions, Retreinamento semanal do Modelo, Implementar logger, etc.
- [ ] Criar um arquivo .md que mostrará as métricas atuais do modelo em produção além de outras métricas.
- [ ] Criar um Dashboard com status dos dados armazenados, além de monitoramento e saúde dos dados.

### **Contribuições:**

Este projeto está na fase ativa de desenvolvimento. Se você está interessado em contribuir ou tem sugestões, crie um problema ou envie um pull request.

---

*Última Atualização: *23/08/2023*


