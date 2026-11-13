# Posto 6 Copacabana — Guia Interativo

Site estático em português, inglês e espanhol. Hospedagem prevista: Cloudflare Pages; o repositório também possui integrações automáticas de preview com Vercel.

## Desenvolvimento

```sh
python scripts/build-covers.py
python -m http.server 8000
```

Os HTML gerados estão versionados: a hospedagem não precisa executar Python. As capas, as páginas de apartamento e as galerias usam templates compartilhados em `templates/`, com os textos nos JSON de conteúdo.

- Capas: `/pt/`, `/en/`, `/es/`, usando `home.css`.
- Apartamento: `/pt/apartamento/`, `/en/apartment/`, `/es/apartamento/`.
- Galeria: `/pt/galeria/`, `/en/gallery/`, `/es/galeria/`.
- Comodidades, localização e contato: páginas internas existentes, no idioma correspondente.

As novas páginas de conteúdo usam `pages.css` e o mesmo padrão de Home e bandeiras da capa. A folha legada `style.css` continua atendendo às demais páginas internas.

Os 15 ícones vêm do sprite aprovado e conservam os mesmos arquivos locais. O recorte circular em CSS oculta o aro dourado incorporado às imagens; o contorno branco, a sombra e o movimento de hover seguem as bandeiras. A foto de Copacabana é local, com autoria e licença em `assets/PHOTO-CREDITS.txt`, acessíveis pelo rodapé fora da capa.

Oito fotos do apartamento foram obtidas do anúncio informado pelo proprietário. Os arquivos ficam em `assets/apartment/`, e as URLs de origem, em `data/apartment-photos.json`.

## Avaliação do Airbnb

`data/airbnb-rating.json` é a fonte única da nota e do número de avaliações para todos os idiomas. Os valores 4,98 e 120 foram confirmados nos dados estruturados públicos de https://www.airbnb.com.br/h/posto6copa, anúncio 48382177.

```sh
python scripts/sync-airbnb-rating.py
python scripts/build-covers.py
```

O script valida tanto a URL canônica quanto o identificador do anúncio. Dados ausentes, inválidos, conflitantes ou falhas de acesso fazem o comando falhar sem sobrescrever o último valor confirmado. Uma leitura sem mudança não altera arquivos nem cria commits.

O workflow `.github/workflows/sync-airbnb-rating.yml` consulta o anúncio a cada seis horas e permite execução manual. Quando os números mudam, atualiza o JSON e os HTML gerados na `main`. A publicação depende da integração GitHub → hospedagem já configurada.

A rotina só é ativada depois de o workflow entrar na branch principal. Requer GitHub Actions habilitado e permissão de escrita do token padrão do workflow. Se a proteção da branch impedir commits automáticos, será preciso adaptar o fluxo para PRs. Agendamentos do GitHub podem atrasar e, em repositórios públicos inativos, ser desativados pela plataforma após 60 dias.

A consulta usa o HTML público normal, sem login nem API privada. Não é uma integração oficial do Airbnb, nem atualização instantânea. Se o Airbnb bloquear a consulta ou mudar o formato dos dados, o job avisará por falha e o site conservará a última informação confirmada. A rotina não sincroniza preço, disponibilidade, fotos ou textos do anúncio.

## Verificação

```sh
python -m unittest discover -s tests -v
```

Com Playwright para Python e Chromium instalados, mantenha o servidor na porta 8000:

```sh
python scripts/verify-covers.py
python scripts/verify-content-pages.py
```

Os testes de navegador cobrem 24 cenários de capa e 24 cenários das novas páginas, os destinos do menu, imagens, a troca de idiomas e os 45 atalhos. Relatórios e capturas ficam em `../work/copacabana-verification/`. Os testes da sincronização verificam falhas de acesso, identificação de anúncio, números inválidos, ausência de alterações e reconstrução dos três idiomas após mudança da nota.

## Publicação

As correções são apresentadas na PR #1, branch `fix/capas-compartilhadas`. A validação local e os previews de revisão não confirmam a publicação de produção no Cloudflare. Após integrar a PR, confira as três capas e os destinos no endereço público, além da primeira execução do workflow de sincronização.
