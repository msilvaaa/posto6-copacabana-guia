# Tempos dos aeroportos até o prédio

Destino: Rua Raul Pompéia, 131, Copacabana, Rio de Janeiro. Origens: Santos Dumont (SDU) e Galeão (GIG, Terminal 2). Estimativas de carro com trânsito, sem contagem regressiva artificial.

A integração está preparada, mas só fornece minutos após configurar uma credencial privada da Google Routes API. Sem ela, a página oferece as duas rotas no Google Maps e não inventa tempos.

Para ativar, habilite a Routes API em um projeto Google Maps com faturamento configurado e adicione `GOOGLE_MAPS_ROUTES_API_KEY` como segredo do ambiente de produção do Cloudflare Pages. Restrinja a chave à Routes API e configure uma quota compatível com o uso desejado. A API é um serviço externo que pode ter cobrança. A chave nunca deve entrar no GitHub ou no HTML. Uma nova publicação ativa a configuração.

A função `/api/airport-transfers` consulta as duas rotas com `TRAFFIC_AWARE` e saída no momento da consulta. Os resultados válidos ficam em cache por 30 minutos por ponto de presença do Cloudflare; o navegador consulta a cada 30 minutos enquanto a página está aberta e volta a consultar ao retornar a uma aba com dados vencidos. Sem visitantes, não há consultas agendadas. Todos os parâmetros de rota são fixos; parâmetros da URL não geram chaves de cache adicionais. Não são enviadas a localização ou informações do visitante.

A tela mostra o instante da consulta no fuso de Brasília. Dados vencidos ou indisponíveis não são exibidos como tempos atuais; os links para o Maps continuam disponíveis. A frequência de consulta não garante que a duração mude a cada atualização.
