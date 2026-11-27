# Guia novo ao lado do projeto antigo

Este Worker encaminha apenas `/guia` e `/guia/*` ao Pages existente. Mantém
`/pt`, `/es`, `/eua`, a raiz e os arquivos do projeto antigo no servidor atual.
Não associe o domínio inteiro ao Pages nem substitua o registro A do projeto antigo.

Os caminhos de HTML, CSS, JavaScript e dados do novo guia são adaptados durante
as respostas. APIs seguem para `/guia/api/*`, mantendo a atualização existente.
A entrada `/guia/` abre `/guia/pt/`; idiomas ficam em `/guia/pt/`, `/guia/es/`, `/guia/en/`.

## Instalação pelo painel

1. Cloudflare → Workers & Pages → Criar aplicativo → Worker.
2. Crie `posto6-guia-router` e abra Editar código.
3. Substitua o código pelo conteúdo completo de `worker.mjs` e implante.
4. Settings → Domains & Routes → Add → Route.
5. Zona: `posto6copacabana.com.br`. Rota: `posto6copacabana.com.br/guia*`.
6. O registro A do domínio precisa permanecer com proxy ativado (nuvem laranja),
   mantendo o IP atual do projeto antigo.
7. Verifique `/guia/`, idiomas, imagens, navegação e APIs. Confirme também
   `/pt` e `/eua` antigos. O endereço espanhol antigo ainda precisa ser confirmado.

Também é possível usar `npx wrangler deploy` nesta pasta, autenticado na conta
correta. A configuração não transfere a propriedade do domínio.

## Desfazer

Remova somente a rota deste Worker. O projeto antigo continuará no seu DNS atual.
O Pages original continua disponível independentemente deste encaminhamento.

## Limites

Todas as requisições encaminhadas, inclusive arquivos, passam pelo Worker e
consomem a cota do plano Workers da conta. O plano Free do domínio e as cotas
Workers são serviços separados. Não habilita serviços pagos automaticamente.

Quando o projeto antigo for encerrado, será necessário preparar outra configuração
para servir o novo guia na raiz e redirecionar `/guia/*` para os endereços definitivos.
