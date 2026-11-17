# Cotações em Informações

As quatro cotações ficam depois das casas de câmbio em ATM / Câmbio. A fonte é AwesomeAPI: USD-BRLT (dólar turismo), USD-ARS (peso argentino), USD-EUR (euro) e USD-BRL (real). Todos usam um dólar como base e o campo bid (compra) da fonte. O cartão com bandeira dos EUA mostra dólar turismo em reais, separado do cartão do real, que mostra o dólar comercial em reais. Mostramos a taxa indicativa de compra e o instante de cada cotação, sem estimar IOF ou tarifas de uma casa de câmbio.

A fonte permite CORS. O navegador consulta diretamente os quatro pares em um único pedido e guarda somente esses dados públicos por 24 horas em armazenamento local. Reabrir a página ou trocar o idioma não faz nova consulta antes do vencimento. Se a aba continuar aberta, a consulta é refeita quando o cache vence; ao voltar para uma aba com dados vencidos, a atualização também é retomada.

A função Cloudflare `/api/exchange-rates` fica como alternativa, com cache de 24 horas. A consulta direta evita a limitação HTTP 429 observada nos endereços de saída compartilhados do servidor. Sem acesso às duas fontes e sem cache válido, a página informa a indisponibilidade e não inventa valores.

Não há horário fixo diário nem consultas em segundo plano sem visitantes. Os horários das cotações são os fornecidos pela fonte e podem permanecer iguais quando o mercado não muda. Não é necessária uma chave da Google Routes API para as cotações; essa chave pertence apenas à integração opcional dos tempos de trânsito dos aeroportos.
