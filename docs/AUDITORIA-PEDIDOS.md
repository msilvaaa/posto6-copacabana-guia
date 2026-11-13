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
