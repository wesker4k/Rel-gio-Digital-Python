# ⏰ Relógio Digital com CustomTkinter

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Framework](https://img.shields.io/badge/Framework-CustomTkinter-purple.svg)

## 📖 Sobre o Projeto

Este é um projeto de um relógio digital de desktop desenvolvido em Python, utilizando a moderna biblioteca *CustomTkinter*. O objetivo foi criar uma aplicação com visual limpo, profissional e de fácil integração com a área de trabalho, graças à sua janela sem bordas e com fundo transparente.

O relógio exibe a hora e a data atualizadas em tempo real e pode ser posicionado em qualquer lugar da tela, servindo como um widget elegante e funcional.

![image](https://github.com/user-attachments/assets/54a5fc25-fe51-4b7c-b85d-adf131ddc1f6)

---

## ✨ Funcionalidades Principais

* *Exibição da Hora em Tempo Real:* Mostra horas, minutos e segundos (HH:MM:SS).
* *Exibição da Data Completa:* Apresenta o dia da semana, dia do mês, mês e ano em português.
* *Interface Moderna e Limpa:* Tema escuro por padrão e fundo transparente para uma integração suave.
* *Fonte Personalizada:* Utiliza a fonte "Digital-7" para um visual clássico de relógio digital.
* *Janela sem Bordas e Arrastável:* Sem a barra de título padrão, a janela pode ser movida livremente pela tela com o mouse.
* *Botão de Fechar Estilizado:* Um botão de fechar customizado que se integra ao design, com efeito hover.
* *Localização:* Configurado para exibir a data no formato pt_BR (Português do Brasil).

---

## 🔧 Tecnologias Utilizadas

* *Python 3*
* *CustomTkinter:* Para a criação da interface gráfica.
* *Módulos Nativos:* time e locale.

---

## 🚀 Como Executar o Projeto

Siga os passos abaixo para executar o relógio em sua máquina.

### *Pré-requisitos*

* *Python 3* instalado em seu sistema.
* A fonte *Digital-7*. Você pode baixá-la gratuitamente em sites como o [DaFont](https://www.dafont.com/digital-7.font).

### *Instalação*

1.  *Clone este repositório:*
    bash
    git clone [https://github.com/wesker4k/nome-do-seu-repositorio.git](https://github.com/wesker4k/nome-do-seu-repositorio.git)
    cd nome-do-seu-repositorio
    

2.  *Instale a dependência (CustomTkinter):*
    bash
    pip install customtkinter
    

3.  *Adicione a fonte:*
    * Crie uma pasta chamada fonts na raiz do projeto.
    * Coloque o arquivo da fonte (digital-7.ttf) dentro desta pasta. A estrutura final deve ser:
    
    /
    ├── RelogioDigital.py
    └── fonts/
        └── digital-7.ttf
    

4.  *Execute a aplicação:*
    bash
    python RelogioDigital.py
    

---

## 🎨 Personalização

Você pode facilmente alterar a aparência do relógio editando estas linhas no arquivo RelogioDigital.py:

```python
# Altere o tema geral para "Light" ou "System"
ctk.set_appearance_mode("Dark") 

# Altere o tema de cores para "dark-blue" ou "green"
ctk.set_default_color_theme("blue")

```
---

##  Desenvolvimento

Este projeto foi desenvolvido por:

| [<img src="https://avatars.githubusercontent.com/u/170688856?v=4" width=115><br><sub>João Pedro Silva Sinhorini </sub>](https://github.com/wesker4k) |
|:----------------------------------------------------------------------------------------------------------------------------------------------------------:|


---

## 📝 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.
