# Correção preparada em 13/11/2026

- `pt/index.html`, `en/index.html`, `es/index.html`: gerados pelo mesmo template, com traduções e destinos próprios.
- `home.css`: estilos consolidados das capas, sem `!important` e sem seletores dependentes do idioma. Desktop preserva a composição PT; até 1100 px o menu fica abaixo da foto para evitar sobreposições.
- `assets/cover-icons/*.png`: 15 imagens independentes extraídas do sprite aprovado, resolução original de 70 × 70.
- `assets/copacabana-drummond.jpg` e `assets/PHOTO-CREDITS.txt`: fotografia local com autoria, fonte e licença registradas.
- `templates/` e `scripts/build-covers.py`: fonte única do layout e textos dos três idiomas.
- `scripts/verify-covers.py`: verificação automatizada em Chromium/Playwright, com código de saída de erro quando alguma verificação falha.
- Menu superior no celular: os seis links ficam visíveis em linhas, sem depender de rolagem horizontal.
- Créditos da fotografia: link no rodapé, fora da capa, traduzido nos três idiomas.

Foram verificados 24 cenários (3 idiomas × 8 larguras), 49 destinos internos HTTP 200, 15 imagens distintas carregadas, alinhamento idêntico dos botões e cabeçalho entre idiomas, ausência de rolagem horizontal e animação do cabeçalho. Os 45 atalhos e as nove combinações de troca de idioma foram abertos com cliques reais no navegador. A fotografia de fundo também foi carregada e decodificada no teste. A verificação final da geometria não apresentou falhas. A geração dos HTML é reproduzível; `git diff --check` passou.

Os links superiores Apartamento/Galeria não tinham páginas correspondentes. Foram direcionados às páginas existentes de boas-vindas/comodidades, respectivamente. Essa escolha deve ser revisada antes da publicação.

O CSS legado das páginas internas foi preservado. A correção está preparada para revisão em uma branch separada; não houve deploy de produção. A validação do site público depois da publicação permanece pendente; este relatório cobre somente a cópia local.
