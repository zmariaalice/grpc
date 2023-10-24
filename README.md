### Passo 1: Instalar o Python

Se você ainda não tem o Python instalado, siga as instruções em python.org para baixar e instalar a versão mais recente do Python.

### Passo 2: Instalar o virtualenv (caso não tenha)

O virtualenv é uma ferramenta que permite criar ambientes virtuais Python. Se você ainda não o tem instalado, você pode fazê-lo usando o pip (gerenciador de pacotes do Python):

```
pip install virtualenv
```

### Passo 3: Criar um Ambiente Virtual

Vamos criar um ambiente virtual com o nome venv. Substitua venv pelo nome que desejar.

```
# No Windows
python -m venv venv

# No macOS e Linux
python3 -m venv venv

```

### Passo 4: Ativar o Ambiente Virtual

Agora, ative o ambiente virtual:

No Windows:

```
venv\Scripts\activate
```

No macOS e Linux:

```
source venv/bin/activate
```

### Passo 5: Instalar Pacotes a partir de requirements.txt

Dentro do ambiente virtual, você pode instalar todos os pacotes listados em um arquivo requirements.txt. Certifique-se de estar no diretório onde o arquivo requirements.txt está localizado e, em seguida, execute o seguinte comando:

```
pip install -r requirements.txt
```

### Passo 6: Desativar o Ambiente Virtual

Quando você terminar de trabalhar no seu projeto e quiser desativar o ambiente virtual, basta executar o seguinte comando:

```
deactivate
```

### Passo 7: Rodar

```
python3 app.py
```
