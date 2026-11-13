# Revisão dos pedidos — 13/11/2026

Escopo: guia Copacabana migrado do Canvas, em português, inglês e espanhol.

| Pedido | Situação verificada |
| --- | --- |
| Eliminar faixas de cabeçalho e rodapé e excesso de espaço | Faixas removidas. Controles compactos sobre a área superior no computador; uma linha mínima no celular evita sobrepor o conteúdo. Anterior/Próximo continuam acessíveis e centralizados. |
| WhatsApp circular, abaixo das imagens à direita, sem texto | Presente nas 106 páginas, com verde em degradê, contorno branco, sombra e movimento ao passar o cursor/focar, iguais aos das bandeiras. |
| Ícones da capa sem dourado e bandeiras padronizadas | Círculos com contorno branco; idiomas e Home únicos em cada página. |
| Início, Apartamento, Comodidades, Galeria e links da capa | Destinos próprios e idioma preservado; seções Apartamento/Galeria/Comodidades compartilham estrutura e retorno ao guia. |
| Anterior/Próximo estáveis e legíveis, inclusive restaurantes e emergência | Controles HTML abaixo da área de leitura; os controles antigos pintados nas artes foram ocultados. |
| Duplicações em Transportes, Informações e Restaurantes | Controles antigos ocultados, um grupo funcional por página; em Informações, controles no computador ficam sobre a foto para preservar os textos. |
| Imagem branca sobre Americanas | Cartão reconstruído com marca oficial e link de mapa preservado. |
| Avaliação 4,98 e 120 comentários, atualizada automaticamente | Valor confirmado no cache; consulta automática ao anúncio a cada seis horas, preservando o último valor válido se a fonte falhar. Não é atualização instantânea. |
| Melhorar todas as fotos | Parcial: oito fotos do apartamento disponíveis até 2560 px e versões responsivas; a foto de boas-vindas usa a original maior. As demais imagens incorporadas nas artes antigas dependem de originais melhores para ganhar detalhe real. |
| Voltar depois de abrir fotos ou links | Fotos abrem no visualizador do guia com botão de retorno. Links externos abrem outra aba, preservando o guia; não é possível inserir nosso botão dentro de sites de terceiros. |
| Previsão do tempo de Copacabana em todas as páginas | Disponível nas 106 páginas; na capa no canto superior e nas internas junto aos controles após o conteúdo. Mostra três dias e data da atualização. Consulta automática a cada seis horas. |
| Remover crédito visível da capa | Crédito abaixo da foto retirado; atribuição da licença preservada discretamente no diálogo de informações do tempo. |
| Título da capa mais alto e reserva mais perto do fim | Título na região clara abaixo da marca; chamada de reserva posicionada abaixo das informações principais. |

## Verificação

Navegador Chromium local: 106 páginas; 103 áreas de leitura com navegação estável; retorno de fotos em três idiomas; previsão em três idiomas; destinos externos preservando o guia. Navegação original: 288 combinações de página/tamanho, 177 cliques e 12 verificações com imagens lentas. Capas e seções adicionais verificadas em resoluções de celular, tablet e computador. Quatorze testes de validação das fontes de avaliação e tempo.

A conferência pública compara as páginas e recursos publicados com os arquivos testados. Resultados detalhados são gerados pelos scripts de verificação em `scripts/`.

## Ajuste posterior solicitado

Temperatura e previsão restritas às três capas, com fundo transparente. As capas exibem o símbolo de Wi-Fi junto ao texto de alta velocidade. Botões de página “Voltar ao guia” e “Ampliar página” removidos das páginas internas; Home, bandeiras e Anterior/Próximo preservados. O retorno do visualizador de fotos permanece disponível ao abrir uma foto. Este ajuste substitui os itens anteriores sobre tempo nas páginas internas e botão separado de retorno.

## Navegação dentro do conteúdo e mensagem do WhatsApp

Por novo pedido, Anterior/Próximo deixam de ocupar uma linha fixa fora da leitura. Nas seções nativas ficam ao final da descrição; nas artes antigas ficam junto ao fim da coluna de descrição, com largura total em telas pequenas para manter a legibilidade. O guia passa a usar toda a altura disponível, sem faixa inferior reservada. Esse comportamento substitui a navegação fixa dos itens anteriores.

WhatsApp abre uma conversa com texto sugerido, sem envio automático:

- Português: Olá, eu gostaria de saber a disponibilidade do apartamento em Copacabana, para aluguel por temporada.
- Inglês: Hello, I would like to check the availability of the apartment in Copacabana for a vacation rental.
- Espanhol: Hola, me gustaría consultar la disponibilidad del apartamento en Copacabana para un alquiler vacacional.

## Ajuste da composição da capa

Símbolo de pessoa caminhando no primeiro destaque, com legenda “A poucos passos da praia de Copacabana” e traduções correspondentes. Botão de reserva reduzido de372 para280px de largura mínima no computador e de280 para230px no celular. Título em uma única linha, sem quebra inserida, com descrição imediatamente abaixo e tamanhos ajustados por idioma e resolução.

## Título acima da estátua e fim da capa

Título elevado, reduzindo o intervalo abaixo da marca e ajustando a posição superior. Símbolo de cama junto a Apartamento completo. WhatsApp incorporado ao canto inferior da própria capa, eliminando sua linha separada; no computador a capa preenche a altura da janela para evitar sobra inferior. Próxima foi deslocado lateralmente para não colidir com WhatsApp. Conferência visual em320,390,1440,1920px: fim da página coincide com a capa, WhatsApp dentro dela e sem colisão com Próxima.

## Índice da capa e temperatura

Índice superior com cinco itens: Início, Apartamento (abre Bem-vindos), Comodidades (abre Comodidades), Localização e Emergência (substitui Galeria). Contato retirado do índice superior. Temperatura deslocada para a região superior direita da foto, acima da posição anteriormente ocupada por Contato; no celular usa o espaço livre da segunda linha do índice. Rotas equivalentes em português, inglês e espanhol. Páginas e botões circulares do guia continuam disponíveis.

## Organização em duas fases e alinhamento superior

Orientação do usuário: fase1 concentra a composição para computador; fase2 será dedicada às adaptações para telas de celulares. A marca Posto6Copacabana sobe para o alto da foto e título/subtítulo passam a começar logo abaixo do índice no computador. Marca e texto ficam independentes na estrutura para permitir esse alinhamento; o fluxo atual em celulares é preservado até a segunda fase.

## Remoção de Contato e novos ícones

Página e botão circular Contato removidos em português, inglês e espanhol. A navegação que apontava para Contato retorna ao início; WhatsApp permanece como canal de comunicação. Check-out usa mala, Transportes usa a foto do ônibus do Rio já presente no guia e Wi-Fi usa símbolo branco nítido sobre degradê azul e verde. A capa passa a ter14 botões e o site103 páginas.

## Controles das páginas internas no padrão da capa

Bandeiras e Home com58px no computador, mesma ordem, alinhamento horizontal, contorno, sombra e efeito de elevação da capa. Anterior/Próximo compactos dentro da arte das páginas principais, em vez de uma linha externa abaixo da imagem. As páginas de instruções usam a região superior livre para preservar o conteúdo; nas seções nativas, navegação e WhatsApp compartilham a área de descrição. Não há mais uma linha exclusiva abaixo do conteúdo para o WhatsApp nas páginas internas. Fotos das páginas principais preenchem a altura disponível quando a janela é mais alta. Links invisíveis duplicados de Home nas instruções removidos.

## Previsão a cada30 minutos

Consulta da previsão programada aos minutos23 e53 de cada hora; a avaliação Airbnb mantém sua consulta a cada6 horas. A janela explica que o horário exibido corresponde à última alteração dos dados da previsão, preservado quando a fonte retorna os mesmos valores. Páginas abertas revalidam o arquivo após30 minutos e ao voltar para a aba se esse período já passou. Só há commit e publicação automática quando dados mudam; falha na fonte preserva a última previsão válida. Execuções programadas dependem da disponibilidade do agendador do GitHub e podem atrasar.
