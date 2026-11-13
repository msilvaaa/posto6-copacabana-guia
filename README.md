# Posto 6 Copacabana — Guia Interativo

Site estático em português, inglês e espanhol. Hospedagem existente: Cloudflare Pages.

## Desenvolvimento

```sh
python scripts/build-covers.py
python -m http.server 8000
```

Abra `/pt/`, `/en/` ou `/es/`. Nenhuma dependência de compilação é necessária na hospedagem: os três HTML gerados estão no repositório.

As capas são geradas a partir de `templates/cover.html`, com textos e destinos de `templates/cover-content.json`. Edite esses arquivos e execute o gerador. O layout usa somente `home.css`, sem regras por idioma e sem `!important`. `style.css` permanece para as páginas internas; sua limpeza global não foi feita para evitar alterações fora do escopo.

Os 15 PNG em `assets/cover-icons/` são recortes exatos, sem ampliação, do sprite aprovado `assets/cover-buttons-sprite.webp` (células de 70 × 70). Não dependem de SVG externo, recortes em CSS ou arquivos no GitHub. A fotografia é uma cópia local do arquivo original do Wikimedia; créditos em `assets/PHOTO-CREDITS.txt`.

Desktop mantém a composição PT de referência: foto, painel à direita, grade 3 × 5 e cabeçalho com Home e bandeiras. Até 1100 px, o painel passa para baixo da capa para evitar a sobreposição dos controles. Textos maiores têm espaço reservado para manter a grade na mesma posição nas três línguas.

Os links superiores de Apartamento e Galeria apontavam para páginas inexistentes. Agora levam, respectivamente, à apresentação de boas-vindas e às comodidades existentes, no idioma selecionado. Não foram criadas páginas novas de apartamento/galeria.

O resumo de continuidade foi mantido somente no ambiente local; ele não faz parte dos arquivos enviados ao GitHub.

## Publicação

As alterações estão na cópia local da branch `fix/capas-compartilhadas`, baseada em `aff2710`. A correção será apresentada em uma pull request para a branch `main`. Revise as capas e os destinos de Apartamento/Galeria antes de integrar a correção. Depois do deploy, confira `/pt/`, `/en/` e `/es/` no endereço público; a validação local não confirma a publicação.

## Verificação local

Com Playwright para Python e Chromium instalados, mantenha o servidor na porta 8000 e execute `python scripts/verify-covers.py`. O teste abre PT/EN/ES em oito larguras (320–1920 px), verifica as imagens, a geometria dos controles, as rotas internas e clica nos 45 atalhos. Os relatórios e capturas ficam em `../work/copacabana-verification/`.
