# Sistema Ateliê da Dona Li

Bem-vindo ao Sistema Ateliê da Dona Li! Este projeto é uma aplicação desktop desenvolvida em Python, utilizando Tkinter para a interface gráfica e SQLite para o armazenamento dos dados. O objetivo é facilitar o cadastro, consulta e gerenciamento de produtos artesanais do ateliê.

## Funcionalidades
- Cadastro de produtos com informações detalhadas (tipo, variante, descrição, materiais, custo, tempo de produção, preço e margem de lucro).
- Visualização dos produtos cadastrados em uma tabela interativa.
- Exclusão de produtos.
- Cálculo automático da margem de lucro.
- Interface moderna com modo noturno.

## Estrutura dos Arquivos

- `frontend.py`: Interface gráfica do sistema. É o ponto de entrada da aplicação.
- `backend.py`: Lógica de acesso ao banco de dados SQLite (CRUD dos produtos).
- `atelie.db`: Arquivo de banco de dados SQLite. Gerado automaticamente ao rodar o sistema.
- `__pycache__/`: Pasta de cache do Python (pode ser ignorada).

## Requisitos
- Python 3.8 ou superior
- Não são necessárias dependências externas além da biblioteca padrão do Python.

## Como Executar

1. **Clone o repositório ou copie os arquivos para uma pasta local.**

2. **Execute o frontend:**

```bash
python3 frontend.py
```

3. O sistema irá criar automaticamente o banco de dados (`atelie.db`) na primeira execução.

4. Utilize a interface para cadastrar, visualizar e excluir produtos.

## Observações
- O arquivo `atelie.db` não deve ser editado manualmente.
- Caso queira reiniciar o banco, basta apagar o arquivo `atelie.db` (todos os dados serão perdidos).
- O sistema foi separado em frontend e backend para facilitar manutenção e futuras expansões (ex: API, testes automatizados).

## Licença
Este projeto é de uso pessoal e educacional. Para outros usos, consulte o autor.

---

Se tiver dúvidas ou sugestões, fique à vontade para abrir uma issue ou entrar em contato!
