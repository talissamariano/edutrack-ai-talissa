"""Lista de 100 frases PT-BR para o post-it 'frase do dia' na Home.

Mix: 70% inspiracional/classicas com autores + 30% leve/cotidiano (sem autor).
Nenhuma dependencia externa: a lista vive aqui mesmo.

Funcao publica: quote_of_the_day(today) -> {"text": ..., "author": ...}
Determinismo: usa dia do ano como indice; mesma frase o dia inteiro.
"""

from __future__ import annotations

import datetime as _dt


QUOTES: list[dict[str, str]] = [
    # --- Inspiracionais / classicas (70) ---
    {"text": "O estudo, a busca da verdade e da beleza são domínios em que nos é consentido sermos crianças por toda a vida.", "author": "Albert Einstein"},
    {"text": "A persistência é o caminho do êxito.", "author": "Charles Chaplin"},
    {"text": "Ninguém ignora tudo. Ninguém sabe tudo. Todos sabemos alguma coisa. Por isso aprendemos sempre.", "author": "Paulo Freire"},
    {"text": "Ensinar não é transferir conhecimento, mas criar as possibilidades para a sua própria produção.", "author": "Paulo Freire"},
    {"text": "O saber a gente aprende com os mestres e os livros. A sabedoria, se aprende é com a vida e com os humildes.", "author": "Cora Coralina"},
    {"text": "Feliz aquele que transfere o que sabe e aprende o que ensina.", "author": "Cora Coralina"},
    {"text": "O que vale na vida não é o ponto de partida e sim a caminhada.", "author": "Cora Coralina"},
    {"text": "Sou um sonhador realista. Acho que tudo vale a pena ser tentado.", "author": "Cora Coralina"},
    {"text": "Tudo vale a pena se a alma não é pequena.", "author": "Fernando Pessoa"},
    {"text": "É o tempo da travessia: e, se não ousarmos fazê-la, teremos ficado, para sempre, à margem de nós mesmos.", "author": "Fernando Pessoa"},
    {"text": "No meio do caminho tinha uma pedra, tinha uma pedra no meio do caminho.", "author": "Carlos Drummond de Andrade"},
    {"text": "Há um tempo em que é preciso abandonar as roupas usadas, que já têm a forma do nosso corpo.", "author": "Carlos Drummond de Andrade"},
    {"text": "Liberdade é uma palavra que o sonho humano alimenta, que não há ninguém que explique e ninguém que não entenda.", "author": "Cecília Meireles"},
    {"text": "Talvez não tenha conseguido fazer o melhor, mas lutei para que o melhor fosse feito.", "author": "Martin Luther King"},
    {"text": "Conhece-te a ti mesmo.", "author": "Sócrates"},
    {"text": "Só sei que nada sei.", "author": "Sócrates"},
    {"text": "A felicidade depende de nós mesmos.", "author": "Aristóteles"},
    {"text": "Somos o que repetidamente fazemos. A excelência, portanto, não é um feito, mas um hábito.", "author": "Aristóteles"},
    {"text": "Educar a mente sem educar o coração não é educação.", "author": "Aristóteles"},
    {"text": "Aprender é a única coisa de que a mente nunca se cansa, nunca tem medo e nunca se arrepende.", "author": "Leonardo da Vinci"},
    {"text": "Não basta saber, é preciso também aplicar; não basta querer, é preciso também fazer.", "author": "Goethe"},
    {"text": "Estudar é uma das mais nobres maneiras de revolucionar o mundo.", "author": "Paulo Freire"},
    {"text": "Educação não transforma o mundo. Educação muda pessoas. Pessoas transformam o mundo.", "author": "Paulo Freire"},
    {"text": "Que ninguém se engane, só se consegue a simplicidade através de muito trabalho.", "author": "Clarice Lispector"},
    {"text": "Liberdade é pouco. O que eu desejo ainda não tem nome.", "author": "Clarice Lispector"},
    {"text": "Enquanto eu tiver perguntas e não houver resposta, continuarei a escrever.", "author": "Clarice Lispector"},
    {"text": "A vida começa todas as manhãs.", "author": "Lya Luft"},
    {"text": "Quem não sonhou um amor não tem direito de chamar-se gente.", "author": "Mario Quintana"},
    {"text": "Quem faz um poema abre uma janela.", "author": "Mario Quintana"},
    {"text": "A vida é o dever que nós trouxemos para fazer em casa.", "author": "Mario Quintana"},
    {"text": "Use os talentos que você possui: os bosques seriam muito silenciosos se nenhum pássaro cantasse a não ser aqueles que cantam melhor.", "author": "Henry van Dyke"},
    {"text": "Comece fazendo o necessário, depois o possível. E você estará fazendo o impossível.", "author": "São Francisco de Assis"},
    {"text": "A jornada de mil milhas começa com um único passo.", "author": "Lao-Tsé"},
    {"text": "Em algum lugar, algo incrível está esperando para ser descoberto.", "author": "Carl Sagan"},
    {"text": "Não somos o que sabemos. Somos o que estamos dispostos a aprender.", "author": "Mary Catherine Bateson"},
    {"text": "A maior recompensa do nosso trabalho não é o que nos pagam por ele, mas aquilo em que ele nos transforma.", "author": "John Ruskin"},
    {"text": "Aprenda a regra como um profissional, para que possa quebrá-la como um artista.", "author": "Pablo Picasso"},
    {"text": "Tudo o que sempre quis estava do outro lado do medo.", "author": "George Addair"},
    {"text": "O sucesso é a soma de pequenos esforços repetidos dia após dia.", "author": "Robert Collier"},
    {"text": "Se você quer viver uma vida feliz, amarre-se a uma meta, não a pessoas ou coisas.", "author": "Albert Einstein"},
    {"text": "A imaginação é mais importante que o conhecimento.", "author": "Albert Einstein"},
    {"text": "A medida da inteligência é a capacidade de mudar.", "author": "Albert Einstein"},
    {"text": "Aprenda com o ontem, viva o hoje, espere pelo amanhã. O importante é nunca parar de questionar.", "author": "Albert Einstein"},
    {"text": "A vida é como andar de bicicleta. Para manter o equilíbrio, você precisa continuar em movimento.", "author": "Albert Einstein"},
    {"text": "Eu não falhei. Encontrei dez mil soluções que não davam certo.", "author": "Thomas Edison"},
    {"text": "Gênio é 1% inspiração e 99% transpiração.", "author": "Thomas Edison"},
    {"text": "A vida é 10% o que acontece com você e 90% como você reage.", "author": "Charles R. Swindoll"},
    {"text": "Você nunca é velho demais para estabelecer outra meta ou sonhar um novo sonho.", "author": "C.S. Lewis"},
    {"text": "Não é a montanha que conquistamos, mas a nós mesmos.", "author": "Edmund Hillary"},
    {"text": "Tente. Falhe. Tente de novo. Falhe melhor.", "author": "Samuel Beckett"},
    {"text": "Não conte os dias, faça os dias contarem.", "author": "Muhammad Ali"},
    {"text": "Eu posso aceitar o fracasso, mas não posso aceitar não tentar.", "author": "Michael Jordan"},
    {"text": "Os obstáculos são aquelas coisas assustadoras que você vê quando tira os olhos do seu objetivo.", "author": "Henry Ford"},
    {"text": "Saber muito não te faz inteligente. A inteligência se traduz na forma que você recolhe, julga e aplica a informação.", "author": "Carl Sagan"},
    {"text": "Não há nada nobre em ser superior a outro homem. A verdadeira nobreza está em ser superior a quem você era ontem.", "author": "Ernest Hemingway"},
    {"text": "Acredite que você pode, e você já está no meio do caminho.", "author": "Theodore Roosevelt"},
    {"text": "Para tudo há uma primeira vez.", "author": "William Shakespeare"},
    {"text": "Cada dia é uma nova chance de mudar sua vida.", "author": "Madre Teresa de Calcutá"},
    {"text": "Nem todos podemos fazer grandes coisas, mas podemos fazer pequenas coisas com grande amor.", "author": "Madre Teresa de Calcutá"},
    {"text": "A coragem é a primeira das qualidades humanas porque garante todas as outras.", "author": "Winston Churchill"},
    {"text": "Um pessimista vê dificuldade em cada oportunidade; um otimista vê oportunidade em cada dificuldade.", "author": "Winston Churchill"},
    {"text": "O sucesso não é definitivo, o fracasso não é fatal: é a coragem para continuar que conta.", "author": "Winston Churchill"},
    {"text": "Quando uma porta se fecha, outra se abre; mas frequentemente olhamos tanto tempo para a porta fechada que não vemos a que se abriu.", "author": "Alexander Graham Bell"},
    {"text": "Se você só faz o que sabe, nunca será mais do que é hoje.", "author": "Walt Disney"},
    {"text": "Se você pode sonhar, você pode realizar.", "author": "Walt Disney"},
    {"text": "Ler é um modo de viver mais.", "author": "Luis Fernando Verissimo"},
    {"text": "O futuro pertence àqueles que acreditam na beleza de seus sonhos.", "author": "Eleanor Roosevelt"},
    {"text": "Não espere por uma crise para descobrir o que é importante em sua vida.", "author": "Platão"},
    {"text": "A coisa mais difícil é a decisão de agir; o resto é meramente tenacidade.", "author": "Amelia Earhart"},
    {"text": "Sem disciplina, não há vida que dê liberdade.", "author": "Augusto Cury"},
    {"text": "Quem caminha sozinho pode até chegar mais rápido, mas aquele que vai acompanhado, com certeza vai mais longe.", "author": "Clarice Lispector"},

    # --- Leve / cotidiano (30) ---
    {"text": "Hoje é um bom dia pra começar de novo.", "author": ""},
    {"text": "Pequenos passos também te levam longe.", "author": ""},
    {"text": "Devagar e sempre, mas sempre indo.", "author": ""},
    {"text": "Cada hora estudada é uma vitória sua.", "author": ""},
    {"text": "Você não precisa ser perfeita, só precisa começar.", "author": ""},
    {"text": "Respira. Você tá indo bem.", "author": ""},
    {"text": "Café + foco = combinação imbatível ☕", "author": ""},
    {"text": "Não compare seu capítulo 1 com o capítulo 20 dos outros.", "author": ""},
    {"text": "Erro faz parte. Aprende, ajusta, segue.", "author": ""},
    {"text": "Sextou. Mas a tarefa não.", "author": ""},
    {"text": "Estuda como se ninguém estivesse vendo.", "author": ""},
    {"text": "Hoje é um ótimo dia pra cumprir aquela meta que você adiou.", "author": ""},
    {"text": "Você é mais capaz do que pensa.", "author": ""},
    {"text": "Cada disciplina concluída é um troféu invisível na estante da sua vida.", "author": ""},
    {"text": "Sem pressa, sem pausa.", "author": ""},
    {"text": "A jornada é longa, mas você está no caminho.", "author": ""},
    {"text": "Foco. Foco. Foco. (Depois um chocolate.)", "author": ""},
    {"text": "Mais um dia, mais uma chance de fazer melhor.", "author": ""},
    {"text": "Quem não desiste, conquista.", "author": ""},
    {"text": "Você não tá atrasada, tá no seu tempo.", "author": ""},
    {"text": "Pequenas tarefas concluídas constroem grandes resultados.", "author": ""},
    {"text": "Estudar agora pra agradecer depois.", "author": ""},
    {"text": "Que o seu cansaço de hoje seja o seu sorriso de amanhã.", "author": ""},
    {"text": "A diferença entre 'ainda não consegui' e 'nunca vou conseguir' é tudo.", "author": ""},
    {"text": "Bebe água. Seu cérebro agradece.", "author": ""},
    {"text": "Faz uma tarefinha, depois faz outra. Isso é tudo.", "author": ""},
    {"text": "Sua trajetória é única. Não troca por nada.", "author": ""},
    {"text": "Hoje é o dia perfeito pra estar exatamente onde você está.", "author": ""},
    {"text": "Calma. Você não precisa fazer tudo de uma vez.", "author": ""},
    {"text": "Lembra: você já passou por outros desafios. Esse também passa.", "author": ""},
]


def quote_of_the_day(today: _dt.date | None = None) -> dict[str, str]:
    """Retorna a frase do dia: mesma o dia inteiro, troca a meia-noite.

    Indice = dia_do_ano % len(QUOTES). Deterministico, sem dependencia externa.
    """
    today = today or _dt.date.today()
    idx = today.timetuple().tm_yday % len(QUOTES)
    return QUOTES[idx]
