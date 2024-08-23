# Brazil Football Datalake

## 1. Objective

The objective of this project is to create an open-source, collaborative, and comprehensive dataset about football in Brazil, encompassing teams, players, matches, coaches, and more. Our mission is to collect and process data from all Brazilian states.

In the first version, our focus is on gathering data exclusively about football clubs. We aim to answer questions such as:

* Which is the oldest team in each state? Which is the oldest team in the country?
* Which is the youngest team in each state? Which is the youngest team in the country?
* What are the most common club names?
* How many clubs are registered in each state?
* Can we visualize all the clubs together on a map?"

## 2. How to Run

You can run this project by following the instructions in the Makefile. Ensure that Docker and Python are installed on your system. The project uses the following technologies: Python, Docker, Docker Compose, Airflow, and DBT.

To start the project with Airflow, execute the following commands:

```
make install_dependencies
make create_shared_network
make start
```

Once all services are running, you can access Airflow through your browser and execute the DAGs. To run the DBT models, simply execute make run in your terminal.

## 3. Docs

Read more about our catalog at the [docs folder](./docs/README.md)

## 4. To Do List

- [X] Collect data From Santa Catarina: [Federação Catarinense de Futebol (FCF)](https://fcf.com.br/) (Under Development)
- [ ] Collect data From Acre: [Federação de Futebol do Estado do Acre (FFAC)](http://ffac.com.br/)
- [ ] Collect data From Alagoas: [Federação Alagoana de Futebol (FAF)](http://futeboldealagoas.net/)
- [ ] Collect data From Amapá: [Federação Amapaense de Futebol (FAF)](http://fafamapa.com.br/)
- [ ] Collect data From Amazonas: [Federação Amazonense de Futebol (FAF)](https://fafamazonas.com.br/)
- [ ] Collect data From Bahia: [Federação Bahiana de Futebol (FBF)](http://www.fbf.org.br/)
- [ ] Collect data From Ceará: [Federação Cearense de Futebol (FCF)](https://futebolcearense.com.br/)
- [ ] Collect data From Distrito Federal: [Federação de Futebol do Distrito Federal (FFDF)](http://ffdf.com.br/)
- [ ] Collect data From Espírito Santo: [Federação de Futebol do Estado do Espírito Santo (FES)](https://futebolcapixaba.com/)
- [ ] Collect data From Goiás: [Federação Goiana de Futebol (FGF)](http://fgf.esp.br/)
- [ ] Collect data From Maranhão: [Federação Maranhense de Futebol (FMF)](http://www.futebolmaranhense.com.br/)
- [ ] Collect data From Mato Grosso: [Federação Mato-Grossense de Futebol (FMF)](http://www.fmfmt.com.br/)
- [ ] Collect data From Mato Grosso do Sul: [Federação de Futebol de Mato Grosso do Sul (FFMS)](https://www.futebolms.com.br/)
- [ ] Collect data From Minas Gerais: [Federação Mineira de Futebol (FMF)](https://www.fmf.com.br/)
- [ ] Collect data From Pará: [Federação Paraense de Futebol (FPF)](http://www.fpfpara.com.br/)
- [ ] Collect data From Paraíba: [Federação Paraibana de Futebol (FPF)](http://www.federacaopbf.com.br/)
- [ ] Collect data From Paraná: [Federação Paranaense de Futebol (FPF)](http://www.federacaopr.com.br/)
- [ ] Collect data From Pernambuco: [Federação Pernambucana de Futebol (FPF)](http://www.fpf-pe.com.br/)
- [ ] Collect data From Piauí: [Federação de Futebol do Piauí (FFP)](https://ffp-pi.com.br/)
- [ ] Collect data From Rio de Janeiro: [Federação de Futebol do Estado do Rio de Janeiro (FFERJ)](http://www.fferj.com.br/)
- [ ] Collect data From Rio Grande do Norte: [Federação Norte-Riograndense de Futebol (FNF)](http://www.fnf.org.br/)
- [ ] Collect data From Rio Grande do Sul: [Federação Gaúcha de Futebol (FGF)](https://fgf.com.br/)
- [ ] Collect data From Rondônia: [Federação de Futebol do Estado de Rondônia (FFER)](http://ffer.com.br/)
- [ ] Collect data From Roraima: [Federação Roraimense de Futebol (FRF)](http://www.frf.com.br/)
- [ ] Collect data From São Paulo: [Federação Paulista de Futebol (FPF)](http://www.fpf.org.br/)
- [ ] Collect data From Sergipe: [Federação Sergipana de Futebol (FSF)](http://fsf.com.br/)
- [ ] Collect data From Tocantins: [Federação Tocantinense de Futebol (FTF)](https://ftf.org.br/)
