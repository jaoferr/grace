# GRACE
## Sistema de recomendação de currículos
GRACE é um sistema inteligente que busca auxiliar profissionais de recursos humanos e recrutamento a encontrar o melhor candidato para uma vaga.

---

## WIP
Este projeto ainda está em fase (extremamente) experimental:
   - novas funcionalidades são adicionadas, testadas e removidas o tempo todo;
   - nem tudo que está disponível funciona como deveria (ou sequer funciona);
   - <i>bugs</i> são muitos e estão em toda parte.

---

## UI & API
GRACE é constituída de duas partes principais:
   - API
      - Desenvolvida em Python, utilizando o <i>framework</i> ```FastAPI```, ```SQLALchemy```, ```MySQL```, ```scikit-learn```, ```nltk``` e ```Apache Tika```.
      - Funciona em formato REST/RPC híbrido, onde cada recurso possui ações específicas, seguindo o padrão ```api/v1/[recurso].[ação]``` .
   - UI (não iniciado)
      - GRACE terá uma interface gráfica intuitiva, que funcionará em qualquer navegador moderno.
      - Detalhes de implementação ainda estão sendo decididos.

---
## Utilização
### Docker (recomendado)
Para subir um ambiente *docker* com todas as dependências já instaladas e configuradas, **clone o repositório** e execute o comando ```docker compose up``` dentro da pasta clonada.

Utilizando um navegador de sua escolha, vá até ```http://localhost:8000/docs``` ou ```http://127.0.0.1:8000/docs``` para acessar a documentação da API.

### Manual
É preciso fornecer um servidor ```MySQL``` e um <i>endpoint</i> ```Apache Tika```. Há um arquivo chamado ```docker_run``` neste repositório que contém comandos para criar e executar <i>containers</i> com as duas aplicações.

Um arquivo exemplo ```.env``` com as configurações necessárias está disponível neste respositório.

É necessário ```python 3.9``` ou superior.

As instruções apresentadas assumem um ambiente ```Linux```.

#### **Subindo um servidor local**
Após instalar e configurar os serviços necessários, ```crie um novo ambiente python e instale as dependencias necessárias```:
   - ```python3.9 -m venv venv```
   - ```source venv/bin/activate```
   - ```pip install -r requirements.txt```

Defina as variáveis de ambiente, conforme o exemplo ```.env_example```.
Inicie o servidor com o comando ```source start_server.sh```.

---

## Outras considerações
Este projeto está sendo desenvolvido durante o curso de Ciência de Dados da FATEC Ourinhos.
