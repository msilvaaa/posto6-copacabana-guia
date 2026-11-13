# Correção preparada em 13/11/2026

As capas PT, EN e ES compartilham um único template e CSS. Os 15 botões usam as mesmas imagens locais e conservam a geometria aprovada no desktop; no celular, o painel passa para baixo da foto e os seis links do menu ficam visíveis.

## Revisão solicitada

- O aro dourado que fazia parte das imagens fica oculto pelo recorte circular em CSS. Contorno branco, sombra e hover seguem o padrão das bandeiras.
- Início abre a capa do idioma; Apartamento e Galeria agora têm páginas próprias. Comodidades, Localização e Contato continuam apontando para suas páginas existentes.
- As novas páginas de apartamento e galeria estão traduzidas e mantêm a seção ao trocar o idioma. A galeria usa oito fotos reais do anúncio, armazenadas localmente com origem registrada.
- Nota 4,98 e 120 avaliações confirmadas no HTML público do anúncio Airbnb 48382177. Um JSON compartilhado alimenta todos os idiomas.
- Workflow preparado para verificar a nota a cada seis horas e regenerar as páginas somente quando houver alteração. A rotina só começa após entrar na main e depende do GitHub Actions e das permissões da branch. Não é sincronização em tempo real nem API oficial.
- Se o Airbnb não fornecer uma leitura válida para esse anúncio, o último valor confirmado é preservado.

## Validação

- 24 cenários de capa, 55 destinos internos HTTP 200, 15 imagens diferentes e fotografia carregada; geometria idêntica dos controles entre idiomas e ausência de rolagem horizontal.
- 45 cliques nos atalhos e nove trocas de idioma das capas.
- 24 cenários de conteúdo em celular, tablet e desktop, 18 cliques nos links superiores e 18 trocas de idioma mantendo Apartamento/Galeria.
- Nove testes da sincronização, incluindo falhas de leitura, nota inválida, anúncio diferente, ausência de mudanças e reconstrução dos textos nos três idiomas após uma mudança simulada.
- Leitura real do Airbnb concluída com 4,98 e 120; segunda leitura não alterou arquivos.
- Geração das nove páginas reproduzível; YAML do workflow válido e git diff --check sem erros.

O CSS legado das outras páginas internas foi preservado. A publicação de produção no Cloudflare e a execução agendada após integração à main permanecem pendentes; os testes relatados são locais. O envio da branch também aciona as integrações Vercel já existentes no repositório.
