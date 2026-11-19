# Revisão visual — 18/11/2026

Foram revisadas as 103 rotas em português, inglês e espanhol. A validação automatizada cobriu 309 layouts em larguras de 390, 1440 e 1920 pixels, com densidade de tela 2. O resultado está em `visual-quality-report.json`.

## Correções

- As 51 páginas de instruções de Comodidades passaram de páginas inteiras em JPEG para títulos, instruções, links e navegação em HTML. As fotografias reais dos equipamentos foram separadas como referências, com proporção preservada e largura limitada à resolução da fonte. Os vídeos existentes e o retorno para Comodidades foram mantidos.
- Os títulos do guia e de Comodidades agora usam a mesma fonte cursiva local, com moldura compacta. O quadro de seis regras também é texto nativo, preservando os seis itens e o aviso sobre hóspedes adicionais.
- Ícones das categorias e das comodidades, bandeiras, monitor ilustrado e marca de Wi-Fi foram substituídos por formas vetoriais. O avião original que o proprietário pediu para preservar permanece no enquadramento aprovado, sem ampliação excessiva.
- O QR Code foi refeito em vetor e decodificado para verificar que continua contendo exatamente a rede e a senha existentes. A animação discreta e a preferência por movimento reduzido foram mantidas.
- As oito fotos originais do anúncio foram recuperadas sem o processamento de ampliação do CDN. Os originais são usados nas páginas e na ampliação da galeria; as variantes locais menores continuam atendendo miniaturas e visualizações proporcionais.
- As fotos principais acompanham a rolagem em altura de tela, evitando que uma página de texto longa estique uma fotografia por toda a altura. A divisão de 50/50 nas páginas internas e 70/30 na capa foi preservada.

## Validação

A revisão encontrou zero painéis de texto ainda montados como uma imagem de página, zero distorções de proporção, zero fotografias técnicas ampliadas além dos pixels disponíveis e zero imagens quebradas nas rotas verificadas. Foram conferidos 1.621 destinos e recursos internos, sem ausências. Os 21 testes Python e os 11 testes Node passaram.

As fotos técnicas antigas são registros reais de resolução limitada. Foram mantidas pequenas e proporcionais, com as orientações em texto ao lado, em vez de inventar detalhes por ampliação. Os ambientes do apartamento não foram recriados.

Para repetir a varredura: `python scripts/audit-visual-quality.py --base http://127.0.0.1:8000`. O argumento opcional `--fixtures` permite testar as mesmas fotografias originais previamente baixadas quando o navegador local não tem acesso direto ao CDN; a galeria e a abertura da foto original também foram verificadas com acesso real ao CDN.

As bandeiras vetoriais são as versões públicas da Wikimedia Commons (Brasil, Espanha e Estados Unidos). Créditos das fotografias de terceiros já existentes permanecem no guia.

## Preferência visual restaurada — 19/11/2026

A pedido do proprietário, as letras originais dos títulos voltaram a ser exibidas em recortes específicos, preservando as fontes e molduras do projeto. As figuras coloridas das categorias e do menu de Comodidades também foram restauradas. Esses recortes decorativos de títulos não são considerados páginas de texto em imagem pela auditoria. As instruções permanecem em HTML, as fotografias mantêm a proporção, e as correções já aprovadas de QR Code, assinaturas, bandeiras e ícones do Check-out foram preservadas.

19/11/2026 — Owner approved new modern colorful icons. Category and amenity pictograms now use crisp filled duotone SVGs with saturated accents; no raster sprite enlargement. Information remains free of enclosing rings; Emergency retains equal-radius circles. Original airplane/phone animation, actual photos, signatures, flags and page-entry data refresh are preserved. A shared `guide-titles.css` applies the compact Welcome/Check-in frame to category, amenity, apartment and gallery headings; original title lettering is cropped to measured ink bounds for consistent visible height and proportional resizing on small screens.
