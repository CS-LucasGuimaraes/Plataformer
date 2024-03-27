# The Ultimate Platformer

Em um mundo repleto de desafios e mistérios, surge o The Ultimate Platformer, um jogo envolvente e cheio de adrenalina. Prepare-se para embarcar em uma jornada emocionante, onde cada passo pode ser um novo desafio ou um encontro com o perigo. Com Plataformas de diferentes Alturas, Obstáculos Mortais e Inimigos Traiçoeiros, cada fase é um teste de habilidade e agilidade.

Você assume o controle de um corajoso personagem, com o objetivo de alcançar a bandeira que marca o próximo nível. Mas cuidado! Cada erro pode custar uma vida, e com apenas três corações, o perigo está sempre à espreita. Explore cenários intricados, supere obstáculos desafiadores enquanto busca a vitória.
Embarque nesta aventura cheia de suspense, onde cada decisão pode ser crucial. Será você capaz de superar todos os desafios e se tornar o mestre do The Ultimate Platformer?


![video2](https://github.com/joseivann/jogo/assets/84510651/f25b0bfd-8eb3-467d-a4eb-6ca39b0a111d)

## 👥 Membros da equipe:
   * Lucas Guimarães Fernandes </lgf> ([CS-LucasGuimaraes](https://github.com/CS-LucasGuimaraes))
   * Marcos Didier Oliveira Neto </mdon> ([marcosdidier](https://github.com/marcosdidier)) 
   * Fernanda Marques Neves </fmn> ([fiefaneves](https://github.com/fiefaneves))
   * Rafael Domingos Nobrega </rdn> ([rafaelnobrega](https://github.com/rafadnobrega))
   * José Ivan Xisto Vilela Junior </jixvj> ([joseivann](https://github.com/joseivann))

## 🎯 Índice

- [👥 Membros da equipe](#-Membros-da-equipe)
- [🎮 Instruções de execução](#-Como-Baixar-e-Jogar)
- [📖 Bibliotecas usadas](#-Bibliotecas-usadas)
- [📋 Divisão de tarefas](#-Divisão-de-tarefas)
- [👨🏻‍💻 Organização do código](#-Organização-do-código)
- [📝 Conceitos](#-Conceitos)
- [🧠 Desafios/Experiência](#-Desafios/Experiência)

## 🎮 Como Baixar e Jogar
  1) Instalar pyGame: abrir o terminal e escrever:  
  ```bash
      pip install pygame
  ``` 
  2) Clone o repositório:
  ```git
      git clone https://github.com/CS-LucasGuimaraes/Platformer.git
  ``` 
  3) Execute o arquivo ``main_menu.py``

<br>

Desenvolvido com plataformas de diferentes alturas, obstáculos e inimigos, o objetivo principal é mover o personagem do jogador da base até a bandeira que indicará o próximo nível. Sua vida e a quantidade de itens coletados apareceram no canto superior da tela.

#### **Link para o codigo fonte**: https://github.com/CS-LucasGuimaraes/Platformer.git

#### **Controles**:
  |            Teclas              |          Descrição           |
  | ------------------------------ | -------------------------- |
  | **W-A-S-D;  &#8592; , &#8593; , &#8594; , &#8595;** | Movimento PC |
  | **Analógico Esquerdo** | Movimento Xbox/PS4 |
  | **Tecla de Espaço** | Pulo PC |
  | **A** | Pulo Xbox |
  | **X** | Pulo PS4 |
  | **ESC** | Pause PC |
  | **Start** | Pause Xbox |
  | **Options** | Pause PS4 |

## 📖 Bibliotecas usadas

#### **PyGame**:
Essa biblioteca consiste em um conjunto de módulos criados com o propósito de facilitar a criação de jogos, possibilitando o desenvolvimento de jogos e aplicativos multimídia utilizando a linguagem Python.

#### **JSON**:
O JSON (JavaScript Object Notation) é uma ferramenta essencial, permitindo o armazenamento e troca eficiente de dados. Com ele, foi possível o armazenamento de dados, como a posição de cada objeto dos níveis, sem que comprometesse a leitura e entendimento do código.

## 📋 Divisão de tarefas

|            Equipe              |          Tarefas           |
| ------------------------------ | -------------------------- |
| **Lucas Guimarães** | Draw Levels, Menu, Game Over, Collectible system, Local Multiplayer, new Assets (Pixel Plataformer), JoyStick Integration, inGame User Interface, Gates System, Enemies, Checkpoints |
| **Marcos Didier** | Draw Levels, Menu, Game Over, Collectible system, new Assets (Pixel Plataformer), Enemies |
| **Fernanda Marques** | Draw Levels, Menu, Game Over, Collectible system, Pause game, Relatório, Gates System |
| **Rafael Domingos** | Draw Levels, Local Multiplayer, new Assets (Pixel Plataformer), Relatório, Checkpoints |
| **José Ivan** | Draw Levels, Local Multiplayer, Relatório, new Assets (Pixel Plataformer) |

## 👨🏻‍💻 Organização do código

#### **A organização do código é composta por diversas partes, sendo as principais**:
- **main_menu.py**:
É responsável por conter a renderização do menu completo, incluindo logo do jogo e 3 botões que direcionam para o New game, Load game e Exit.

-  **game.py**: 
Abriga as linhas responsáveis pela renderização de nível, coletáveis e inimigos. Também contendo as funções de controle de câmera e dos processamentos de eventos.

- **editor.py**:
Contém o modo editor, em que é possível adicionar, excluir e editar tiles nas diferentes fases. Essa função foi de grande relevância ao nosso tradibalho pois possibilita trazer mais nâmica e facilidade para a criação de novos níveis que explorem a criatividade e o tamanho do desafio que se deseja propor.

#### **Em seguida, temos os arquivos que dão suporte aos principais (/scripts)**:
- **utils.py**:
Desenvolvimento das funções de carregamento de imagens, sons, classe de animações, manipulação dos arquivos em .json e restart level.

- **assets.py**:
Armazenamento em dicionários das imagens de cada objeto carregada, além dos sons de cada ação executada pelos players.

- **entities.py**:
No qual se desenvolve a classe de física dos objetos, estruturando colisões, itens coletáveis, além de colisões com inimigos e obstáculos. Temos ainda, a classe do player, a qual herda a classe anterior e adiciona algumas funções, como a de pulo do jogador, contagem de vida. E por fim, a classe do inimigo, que também herda a classe física.

- **tilemap.py**:
Nesse arquivo, encontramos a divisão dos tiles em sets, o qual melhora a performace do jogo, visto que diminui o tempo de iteração, além de ser de fácil manipulação visto que cada set admite um comportamento ordenado por função. Logo, se futuramente for necessário a adição de algum outro objeto, basta que seja incluído no set correspondente. 

- **ui.py**:
Aqui temos a classe responsável pela contagem de coletáveis, como quantidade de moedas, chaves e diamantes.

#### **Ainda dentro de scripts temos uma pasta específica para arquivos de suporte para o menu (/scripts/menu)**:
- **utils.py**:
Desempenha o mesmo papel que o arquivo utils citado anteriormente, só que com exclusividade para o menu.

- **home_screen.py**:
Nele temos o posicionamento dos botões iniciais e o controle de movimentos caso o usuário esteja usando o joystick

- **character_selection.py**:
Caso seja selecionada a opção "Load Game", o usuário é direcionado para a tela que é renderizada nesse arquivo, no qual pode-se notar a presença de paineis que exibem o saves, armazenados em um arquivo json.

- **save_override.py**:
Se for solicitada a sobreposição de um save anterior, essa classe é chamada e zera os dados armazenados no arquivo json do game escolhido.

- **game_over.py**:
Quando o player morre, é dada a ele 3 opções: Restart, Exit ou Back to Menu. Nesse arquivo, é desenvolvido tal ação e como proceder com cada escolha.

- **pause.py**:
É responsável por conter a estruturação do comando de pause do jogo.

#### **Por fim, encontra-se o armazenamento do jogo**:

- **(/saves) & (/levels)**:
Encontramos os arquivos .json, nos quais armazenamos os dados de saves de jogos anteriores e o mapa de cada level.

- **(/data)**:
Armazenamento de fontes, imagens e sons solicitados durente o código do jogo. 

## 📝 Conceitos

#### **Estruturas Condicionais**:
 
 -
 -
 -
 -
 -
 
####  **Laços**:

Dentro do jogo, é possível empregar essas estruturas no código através dos comandos For e While. Eles possibilitam a repetição de instruções até que uma condição seja alcançada. 

-
-
-
-

#### **Loops**:

-
-
-
-
-
 

## 🧠 Desafios/Experiência

 **Maiores desafios**:

Os maiores desafios enfrentados pela nossa equipe foram o uso de ferramentas como Pygame, Github, Programação Orientada a Objetos, dado que a maioria dos membros tinha pouca ou nenhuma experiência anterior com essas ferramentas.

Além disso, a utilização dessas ferramentas era indispensável, o que nos levou a aprender o básico rapidamente para iniciar o desenvolvimento do projeto, e acabou nos proporcionando uma aprendizagem diversificada, desde a criação de elementos simples, como um quadrado móvel na tela, até a elaboração de um jogo mais complexo, que era o objetivo do nosso projeto.

 **Maiores erros cometidos**:

Acreditamos que um dos nossos erros significativos foi a coordenação do trabalho em equipe, quem vai fazer o que, como cada pessoa vai fazer a sua parte, a integração das partes desenvolvidas e a resolução de alguns bugs durante o processo.

 **Lições aprendidas**:

Durante o projeto, aprendemos duas lições fundamentais. Primeiramente, compreendemos a importância do planejamento e da organização da equipe. Além disso, outro aspecto significativo que aprendemos foi a importância em reconhecer que sempre há algo a aprender e que a ajuda de outras pessoas pode ser fundamental para o progresso do projeto.
