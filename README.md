# 🚀 Copiador de Textos Rápidos (QuickText-Copier)

Uma aplicação de desktop desenvolvida em Python com Tkinter e ttkbootstrap para gerenciar e copiar rapidamente snippets de texto, otimizando o fluxo de trabalho e a produtividade diária.

---

## 📸 Screenshot

![image](https://github.com/user-attachments/assets/af1f1fbf-7c59-4422-b823-7d8c18918bb5)


---

## ✨ Funcionalidades

- **Gerenciamento Completo:** Adicione, edite e remova textos personalizados de forma intuitiva.
- **Cópia Rápida:** Copie qualquer texto para a área de transferência com um único clique.
- **Busca Inteligente:** Uma barra de busca que filtra a lista em tempo real conforme você digita.
- **Organização Flexível:** Mova os itens para cima ou para baixo para priorizar os textos mais usados.
- **Integração com o Sistema:** Minimize o aplicativo para a bandeja do sistema (system tray) para acesso rápido sem ocupar espaço na barra de tarefas.
- **Interface Moderna:** Desenvolvido com ttkbootstrap para um visual agradável e com suporte a temas.
- **Persistência de Dados:** Todos os seus textos e a ordem da lista são salvos automaticamente em um arquivo `textos.json`.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.11**
- **Tkinter** (biblioteca de interface gráfica nativa do Python)
- **ttkbootstrap:** Para temas e widgets modernos.
- **pystray:** Para a funcionalidade de bandeja do sistema.
- **Pillow (PIL):** Para manipulação da imagem do ícone.
- **pyperclip:** Para acesso à área de transferência de forma multiplataforma.

---

## 📋 Pré-requisitos

Antes de começar, você precisará ter o **Python 3.11** (ou superior) instalado em seu sistema.

---

## 🚀 Instalação e Execução

Siga os passos abaixo para configurar e rodar o projeto em sua máquina.

1. Clone o repositório:
    ```bash
    git clone https://github.com/CarlosNatanael/QuickText-Copier.git
    cd QuickText-Copier
    ```
2. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
3. Execute o aplicativo:
    ```bash
    python main.py
    ```

---

## 💡 Como Usar

- **Buscar:** Comece a digitar na caixa de busca no topo para filtrar a lista.
- **Copiar:** Selecione um item na lista e clique no botão azul "Copiar Texto Selecionado".
- **Organizar:** Selecione um item e use os botões ▲ e ▼ ao lado da lista para alterar sua posição.
- **Gerenciar:** Use os botões "Adicionar", "Editar" e "Remover" para gerenciar sua coleção de textos.
- **Minimizar:** Clique no "X" da janela para enviá-la para a bandeja do sistema. Clique com o botão direito no ícone na bandeja para restaurar a janela ou fechar o programa definitivamente.

---

## 📂 Estrutura do Arquivo de Dados (`textos.json`)

Os dados são salvos em uma lista de dicionários, o que permite que a ordem seja preservada.

```json
[
     {
          "titulo": "Exemplo de Título 1",
          "texto": [
                "Esta é a primeira linha do texto.",
                "Esta é a segunda linha."
          ]
     },
     {
          "titulo": "Outro Título",
          "texto": [
                "Um texto que contém apenas uma linha."
          ]
     }
]
```

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
